from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout , update_session_auth_hash
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator




# Create your views here.
def home(request): 
    products = Product.objects.all().filter(new_product=True).order_by('-new_product','-quantity')
    context = {'new_product': products}
    return render(request,'store/home.html',context)

def registerPage(request):
    form = RegisterPage()
    if request.method == 'POST':
        form = RegisterPage(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():  
                messages.error(request,'Email is already exists')
                return redirect('register-page')
            else:
                form.save()
                return redirect('/account/login')
    else:
        form = RegisterPage()
    context = {'form': form}

    return render(request,'store/register.html', context)


def loginPage(request):
    if request.method=='POST':
        form=AuthenticationForm(data = request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(request,username=username, password=password)
            if user is not False:
                login(request, user)
                return redirect('/')
            else:
                return redirect('register-page')
    else:
        form=AuthenticationForm()
    context = {'form': form}
    return render(request,'store/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login-page')

# product page and fillter by category
def productsPage(request,category_name=None):
    name_category = None
    allProducts = None
    if category_name!=None:
        name_category = get_object_or_404(Category,name=category_name)
        allProducts = Product.objects.all().filter(category_name=name_category).order_by('-quantity','-updated_on')  
    else:
        allProducts = Product.objects.all().order_by('-quantity','-updated_on')
        
    # manage paginator 1 page show 8 product 
    p = Paginator(allProducts, 8)
    try:
        page_number = request.GET.get('page')
        page = p.get_page(page_number)
    except :
        page = 1
    context = {'allProducts':allProducts,'name_category':name_category,'page':page}
    return render(request,'store/products.html',context)

def productById(request, product_id=None):
    id_product=None
    if product_id!=None:
        # get product by id
         id_product = get_object_or_404(Product,id = product_id)

    context={'product':id_product}
    return render(request,'store/product.html',context)

# manage card with session

def _card_id(request):
    card = request.session.session_key
    if not card:
        card = request.session.create()
    return card

@login_required(login_url='login-page')
def addCard(request,product_id):
    # ดึงไอดีสินค้ามาใช้งาน
    id_product = Product.objects.get(id = product_id)
    #ดูว่าสร้างตระกร้าสินค้าแล้วยัง
    try:
        #ถ้าเคยมีตระกร้าสินค้านั้นอยู่แล้ว
        card = Card.objects.get(card_id = _card_id(request))
    # ถ้ายังไม่เคย ให้สร้างตระกร้าสินค้าขึ้นมา
    except Card.DoesNotExist:
        card = Card.objects.create(card_id=_card_id(request))
        card.save()
    #เช็คว่าซือสินค้าซ้ำมั้ย
    try:    
        card_item = CardItem.objects.get(product=id_product,card = card)
        # check ปริมาณสินค้าว่าซื้อเกินที่stockไว้มั้ย
        if card_item.quantity < card_item.product.quantity:
        # ถ้าซ้ำ ปริมาณสินค้าจะเพิ่มขึนทีละ 1
            card_item.quantity += 1
            card_item.save()
    #ถ้าาสินค้าตัวนั้นไม่ได้อยู่ในตระกร้าให้สร้างขึ้นมาใหม่      
    except CardItem.DoesNotExist:
        card_item = CardItem.objects.create(product = id_product, card = card, quantity = 1)
        card_item.save()
    return redirect('/carddetail')

@login_required(login_url='login-page')
def cardDetail(request):
    if request.user.is_authenticated:
        username = str(request.user.username)
        email = str(request.user.email)
        
        total = 0
        counter = 0
        card_items = None
        try:
            card = Card.objects.get(card_id=_card_id(request)) #ดีงตระกร้าจากuserมา ที่แผงไปกับsession นั่นแหละ
            card_items = CardItem.objects.filter(card = card) #ดึงข้อมูลจากตระกร้ามา
            for item in card_items:
                if item.product.premium_price != None:
                    total += item.product.premium_price*item.quantity
                    counter += item.quantity
                else:
                    total += item.product.normal_price*item.quantity
                    counter += item.quantity
        except Exception as e:
            pass
        
        form = OrderForm()
        if request.method == 'POST': 
            form = OrderForm(request.POST)
            if form.is_valid():
                # print(request.POST)
                name = request.POST['name']
                address = request.POST['address']
                city = request.POST['city']
                postcode = request.POST['postcode']
                tel = request.POST['tel']
                order = Order.objects.create(
                    username = username,
                    email = email,
                    name = name,
                    address = address,
                    city = city,
                    postcode = postcode,
                    total = total,
                    tel = tel,
                )
                order.save()
                
                for item in card_items:
                    if item.product.premium_price != None:
                        price = item.product.premium_price
                    else:
                        price = item.product.normal_price
                    order_item = OrderItem.objects.create(
                        order = order,
                        category = str(item.product.category_name),
                        product = item.product.brand_name,
                        color = item.product.color,
                        quantity = item.quantity,
                        price = price,
                    )
                    order_item.save()
                    
                    product=Product.objects.get(id=item.product.id)
                    product.quantity = int(item.product.quantity - order_item.quantity)
                    product.save()
                    item.delete()
                    messages.success(request,'Your order has been sent to vender successfully')
                return redirect('card-detail')
    context = {'card_items':card_items,'total':total,'counter':counter,'form':form}
    
    return render(request,'store/carddetail.html',context) 


def removeCard(request,product_id):
    # ดึงตระกร้าสินค้ามา
    card = Card.objects.get(card_id = _card_id(request))
    # ดึง product by id มา
    id_product = Product.objects.get(id = product_id)
    # เอาทั้ง 2 มาเก็บไว้ในcard items  แล้วเวลาลบก็ลบจาก card_items นี่แหละ
    card_items = CardItem.objects.get(product = id_product , card = card)
    card_items.delete()
    return redirect('/carddetail')

def orderHistory(request):
    if request.user.is_authenticated:
        username = str(request.user.username)
        orders = Order.objects.filter(username=username).order_by('-id')
        
    p = Paginator(orders, 6)
    try:
        page_number = request.GET.get('page')
        page = p.get_page(page_number)
    except :
        page = 1
    context = {'orders':orders,'page':page}
    return render(request,'store/history.html',context)

def viewOrder(request,order_id):
    id_order=None
    if request.user.is_authenticated:
        username = str(request.user.username)
        if order_id!=None:
            # get product by id
            id_order = get_object_or_404(Order,username=username,id = order_id)
            item_order = OrderItem.objects.filter(order = id_order)
    context={'item_order':item_order,'id_order': id_order}
    return render(request,'store/vieworder.html',context)
    
    

@login_required
def profile(request):
    u_form = UserUpdateForm()
    p_form = UserProfileForm()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance= request.user.profile)

    context = {'user_form': u_form,'profile_form': p_form}
    return render(request,'store/profile.html', context)
    
def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your Password has been changed successfully!')
            return redirect('change-password')
        else:
            messages.error(request,'Please correct the error below.')
    else:
        form = ChangePassword(request.user)
    context = {'form':form}
    return render(request,'store/change_password.html', context)


def payment(request):
    form = PaymentForm()
    if request.method=='POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
           form.save()
        messages.success(request,'Your payment has been sent successfully')
        return redirect('payment-page')
    else:
        form = PaymentForm()
    context = {'form': form}
    return render(request, 'store/payment.html',context)

def thank(request):
    return render(request,'store/thank.html')

def howtoOrder(request):
    return render(request, 'store/howto_order.html')





    
    
        

         
                
            
    
            
            
             
             
         
    
    
    



