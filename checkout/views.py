from django.shortcuts import render, redirect, get_object_or_404
from order.models import Order, Cart
from .models import BillingAddress
from .forms import BillingAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views import generic
import datetime
from django.utils.crypto import get_random_string

import stripe


@login_required
def checkout(request):
    """
    Saving address, Order items and order total
    """
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
# Save address for future use
    form = BillingAddressForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, f'Delivery Address Saved')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderItems.all()
    order_total = order_qs[0].get_totals()
    return render(request, 'checkout/checkout.html',
                  context={'form': form, 'order_items': order_items,
                           'order_total': order_total,
                           'saved_address': saved_address})

"""
Stripe secret key from settings.py file
"""
stripe.api_key = settings.STRIPE_SECRET_KEY


def payment(request):
    """
    Stripe public key from settings.py file
    Get total cost from order items
    """
    key = settings.STRIPE_PUBLIC_KEY
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_total = order_qs[0].get_totals()
    totalCost = float(order_total * 100)
    total = round(totalCost, 2)
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=total,
                                      currency='GBP',
                                      description=order_qs,
                                      source=request.POST['stripeToken'])
        print(charge)
    return render(request, 'checkout/payment.html',
                  {"key": key, "total": total})


def charge(request):
    """
    Once payemnt processed, order id and payment id is saved
    Items will be removed from cart
    """
    order = Order.objects.get(user=request.user, ordered=False)
    orderitems = order.orderItems.all()
    order_total = order.get_totals()
    totalCost = int(float(order_total * 100))
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=totalCost,
            currency='GBP',
            description=order,
            source=request.POST['stripeToken']
        )

        print(charge)

        if charge.status == "succeeded":
            orderId = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            print(charge.id)
            order.ordered = True
            order.paymentId = charge.id
            order.orderId = f'#{request.user}{orderId}'
            order.save()
            cartItems = Cart.objects.filter(user=request.user)
            for item in cartItems:
                item.purchased = True
                item.save()
        return render(request, 'checkout/charge.html', {"items": orderitems,
                                                        "order": order})


@login_required
def orderView(request):
    """
    Shows orders that have been processed
    """
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {
            'orders': orders,
        }
    except:
        messages.warning(request, 'You do not have an active order')
        return redirect('home')
    return render(request, 'checkout/order.html', context)
