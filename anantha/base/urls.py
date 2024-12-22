
from django.contrib import admin
from django.urls import path,include
from . import views as v

app_name = 'base'
urlpatterns = [
    path('',v.index,name='index'),
    path('contact',v.contact,name='contact'),
    path('mycart',v.mycart,name='mycart'),
    path('items',v.items,name='items'),
    path('update',v.update,name='update'),
    path('update/<int:pk>/',v.update_dress,name='update-dress'),
    path('add-dress',v.adddress,name='add-dress'),
    path('ipage/<int:pk>/',v.ipage,name='ipage'),
    path('remove_from_cart/<int:item_id>/', v.remove_from_cart, name='remove_from_cart'),
    path('order_confirmation', v.order_confirmation, name='order_confirmation'),
    path('checkout/', v.checkout, name='checkout'),
]
