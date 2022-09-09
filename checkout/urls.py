from django.urls import path
from .import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    # path('pay/', views.payment, name='payment'),
    # path('success/', views.success, name='success'),
    # path('cancel/', views.cancel, name='cancel'),
    path('create-checkout-session', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('payment-success', views.paymentSuccess, name='payment-success'),
    path('payment-cancel', views.paymentCancel, name='payment-cancel'),
    # path('webhook/stripe', views.my_webhook_view, name='webhook-stripe'),
]