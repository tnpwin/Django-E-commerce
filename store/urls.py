from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home-page'),
    path('account/register/',registerPage,name='register-page'),
    path('account/login/',loginPage,name='login-page'),
    path('account/logout/',logoutPage,name='logout-page'),
    path('account/orderHistory/',orderHistory,name='history-page'),
    path('account/orderHistory/<int:order_id>',viewOrder,name='order-detail'),
    path('account/profile/',profile,name='profile'),
    path('account/profile/change',change_password,name='change-password'),
    path('products/',productsPage,name='products-page'),
    path('howto/',howtoOrder,name='howto-page'),
    path('category/<str:category_name>',productsPage,name='product_by_category'),
    path('products/<int:product_id>',productById,name='product'),
    path('card/add/<int:product_id>',addCard,name='addCard'),
    path('carddetail/',cardDetail,name='card-detail'),
    path('card/remove/<int:product_id>',removeCard,name='removeCard'),
    path('payment',payment,name='payment-page'),    
    
]













