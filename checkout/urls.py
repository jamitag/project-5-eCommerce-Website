from django.urls import path
from .import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('charge/', views.charge, name='charge'),
    path('order-view/', views.orderView, name='orders'),
]
