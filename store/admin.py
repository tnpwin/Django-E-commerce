from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display=['category_name','brand_name','relative_image','color','premium_price','normal_price','quantity']
    list_editable =['color','premium_price','normal_price','quantity']
    list_filter=('category_name',)
    list_per_page = 10
admin.site.register(Product,ProductAdmin)

admin.site.register(Card)

class CardItemsAdmin(admin.ModelAdmin):
    list_display=['quantity']

admin.site.register(CardItem)

class OrderAdmin(admin.ModelAdmin):
    list_display=['username','name','address','city','postcode','tel','email','total','updated_on']
    list_per_page = 15
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display=['order','category','product','color','quantity','price','created_on','updated_on']
    list_per_page = 15

admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(Profile)

class PaymentAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display=['order_number','first_name','last_name','method','date','month','slip','amount']
    list_filter=['month']
admin.site.register(UserPayment,PaymentAdmin)







