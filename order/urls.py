from django.urls import path
from .import views

urlpatterns = [
    path('add-to-cart/<pk>/', views.add_to_cart, name='add_to_cart'), 
    path('cart/', views.cart_view, name='cart'),
    path('remove/<pk>/', views.remove_from_cart, name='remove'),
    path('increase/<pk>/', views.increase_cart, name='increase'),
    path('decrease/<pk>/', views.decrease_cart, name='decrease'),
]