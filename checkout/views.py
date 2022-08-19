from django.shortcuts import render, HttpResponseRedirect
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

    form = BillingAddressForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, f'Delivery Address Saved')
    return render(request, 'checkout/checkout.html', context={'form':form})

