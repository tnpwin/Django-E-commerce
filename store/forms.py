
from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import FileInput

from store.models import *


class RegisterPage(UserCreationForm):
    username = forms.CharField(max_length=150,required=True)
    email = forms.EmailField(max_length=150,required=True)
    class Meta:
        model = User
        fields  =['username','email','password1','password2']
        
class OrderForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=255, required=True)
    postcode = forms.CharField(max_length=255)
    telephone = forms.CharField(max_length=255)
    
    class Meta:
        model = Order
        fields = ['name','address','city','postcode','telephone']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=150, required=False)
    last_name = forms.CharField(label='Last Name', max_length= 150, required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {'avatar': FileInput(),}
        
class ChangePassword(PasswordChangeForm):
    class Meta:
        model = User
        fields  = "__all__"
        
    
        
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = UserPayment
        fields = "__all__"
        widgets = {'slip': FileInput(),}

        

    

        

    
        
    


