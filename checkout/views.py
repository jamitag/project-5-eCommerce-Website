from django.shortcuts import render, HttpResponseRedirect, redirect
from order.models import Order
from .models import BillingAddress
from .forms import BillingAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse


# Create your views here.

@login_required
def checkout(request):
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
    return render(request, 'checkout/checkout.html', context={'form':form, 'order_items':order_items, 'order_total':order_total, 'saved_address':saved_address})

stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'https://8000-jamitag-project5-g004aetgzau.ws-eu63.gitpod.io'

@csrf_exempt
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request, 'Please complete delivery address')
        return redirect('checkout')

    if not request.user.profile.is_fully_filled():
        messages.info(request, 'Please complete profile')
        return redirect('users-profile')

    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = [{
            'price_data':{
                'currency':'GBP',
                'product_data':{
                    'name':'MAAP PRIME STOW VEST',
                },
                'unit_amount':100,
            },
            'quantity':1,
        }],
        mode = 'payment',
        success_url = YOUR_DOMAIN + '/success',
        cancel_url = YOUR_DOMAIN + '/cancel',
    )
    # return render(request, 'checkout/payment.html', context={})

    return JsonResponse({'sessionId':session.id})


def success(request):
    return render(request, 'checkout/success.html')

def cancel(request):
    return render(request, 'checkout/cancel.html')