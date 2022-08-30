from django.shortcuts import render, HttpResponseRedirect, redirect
from order.models import Order
from .models import BillingAddress
from .forms import BillingAddressForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required

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


@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request, 'Please complete delivery address')
        return redirect('checkout')

    if not request.user.profile.is_fully_filled():
        messages.info(request, 'Please complete profile')
        return redirect('users-profile')
    return render(request, 'checkout/payment.html', context={})

