from django.urls import path
from .import views

urlpatterns = [
    path('add-to-cart/<pk>/', views.add_to_cart, name='add_to_cart'), 
]