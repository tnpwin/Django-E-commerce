from datetime import datetime
from pyexpat import model
from django.urls import reverse
from turtle import update
from django.db import models
from django.contrib.auth.models import User
import calendar



# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    avatar = models.ImageField(default='default.png',upload_to='avatar')
    
    def __str__(self):
        return f'{self.user.username} Profile'

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name_plural='หมวดหมู่ประเภทสินค้า'
        verbose_name='ประเภทสินค้า'

    def __str__(self): 
        return self.name


    def get_url(self):
        return reverse('product_by_category',args =[self.name])


class Product(models.Model):
    category_name = models.ForeignKey(Category,on_delete=models.CASCADE)
    relative_image = models.ImageField(upload_to='product',null=True, blank=True)
    brand_name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    premium_price = models.IntegerField(null=True, blank=True)
    normal_price = models.IntegerField()
    quantity = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    new_product = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_on']
        verbose_name_plural='ข้อมูลสินค้า'
        verbose_name='สินค้า'

    def __str__(self):
        return self.brand_name


class Card(models.Model):
    card_id = models.CharField(max_length=100,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table ='Card'
        ordering = ['-created_on']
        verbose_name_plural='ข้อมูลตระกร้าสินค้า'
        verbose_name='ตระกร้าสินค้า'

    def __str__(self):
        return self.card_id

class CardItem(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def sub_total(self):
        if self.product.premium_price != None:
            return self.product.premium_price * self.quantity
        else:
            return self.product.normal_price * self.quantity
    
    class Meta:
        db_table ='CardItem'
        verbose_name_plural='รายการสินค้าในตระกร้า'
        verbose_name='ข้อมูลสินค้าในตระกร้า'

    def __str__(self):
        return '{}  {} | color:{}| quantity:{}'.format(self.product.category_name,self.product.brand_name, self.product.color,self.quantity)

class Order(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,blank=True,null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    total = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    tel = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'Order'
    
    def __str__(self):
        return str(self.id)
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    product = models.CharField(max_length=255)
    color = models.CharField(max_length=100,default='null')
    quantity = models.IntegerField()
    price = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Order_item'
    
    def sub_total(self):
        return self.quantity * self.price
    
    def __str__(self):
        return self.product

class UserPayment(models.Model):
    
    PAYMENT_SELECTION = (
        ('KTB','KTB 984-5-70890-0'),
        ('K-BANK','K-BANK 984-5-70890-0')
    )
    MONTH_CHOICE = [(str(i), calendar.month_name[i]) for i in range(1,13)]
    
    DATE_CHOICE = [(str(i), str(i)) for i in range(1,32)]
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=255,blank=True)
    method = models.CharField(max_length=50 , choices=PAYMENT_SELECTION)
    date = models.CharField(max_length=30, choices=DATE_CHOICE,default='1')
    month = models.CharField(max_length=20,choices=MONTH_CHOICE,default='1')
    slip = models.ImageField(upload_to='slip')
    amount = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'User_Payment'
        verbose_name_plural='ข้อมูลการชำระเงิน'
        verbose_name='การชำระเงิน'
        
    def __str__(self):
        return str(self.id)
    
    
        

    
    
    

    
    








    










