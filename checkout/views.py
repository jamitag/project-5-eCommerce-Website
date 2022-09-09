from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from order.models import Order
from .models import BillingAddress
from .forms import BillingAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views import generic
import datetime

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

# stripe.api_key = settings.STRIPE_SECRET_KEY
# YOUR_DOMAIN = 'https://8000-jamitag-project5-g004aetgzau.ws-eu63.gitpod.io'

# @csrf_exempt
# def payment(request):
#     saved_address = BillingAddress.objects.get_or_create(user=request.user)
#     if not saved_address[0].is_fully_filled():
#         messages.info(request, 'Please complete delivery address')
#         return redirect('checkout')

#     if not request.user.profile.is_fully_filled():
#         messages.info(request, 'Please complete profile')
#         return redirect('users-profile')

#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     session = stripe.checkout.Session.create(
#         payment_method_types = ['card'],
#         line_items = [{
#             'price_data':{
#                 'currency':'GBP',
#                 'product_data':{
#                     'name':'MAAP PRIME STOW VEST',
#                 },
#                 'unit_amount':100,
#             },
#             'quantity':1,
#         }],
#         mode = 'payment',
#         # success_url = YOUR_DOMAIN + '/success',
#         # cancel_url = YOUR_DOMAIN + '/cancel',
#         success_url = request.build_absolute_uri(reverse('success')
#         ) + "?session_id = {CHECKOUT_SESSION_ID}",
#         cancel_url = request.build_absolute_uri(reverse('cancel')
#         )
#     )
#     # return render(request, 'checkout/payment.html', context={})

#     return JsonResponse({'sessionId':session.id})


# def success(request):
#     return render(request, 'checkout/success.html')

# def cancel(request):
#     return render(request, 'checkout/cancel.html')


stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'https://8000-jamitag-project5-g004aetgzau.ws-eu64.gitpod.io'

class CreateCheckoutSessionView(generic.View):
    def post(self, *args, **kwargs):
        # host = self.request.get_host()

        order_id = self.request.POST.get('order-id')
        order = get_object_or_404(Order, orderId=order_id)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price_data': {
                        'currency':'GBP',
                        'unit_amount': Decimal(order.get_totals() * 100),
                        'product_data': {
                            'name': order.id,
                        },
                    },
                    'quantity':1,
                },
            ],
            mode = 'payment',
            # success_url = "http://{}{}".format(host, reverse('payment-success')),
            # cancel_url = "http://{}{}".format(host, reverse('payment-cancel')),
            success_url=YOUR_DOMAIN + '/payment/payment-success',
            cancel_url=YOUR_DOMAIN + '/payment/payment-cancel',
        )

        return redirect(checkout_session.url, code=303)

def paymentSuccess(request):
    context = {
        'payment_status':'success',
    }

    return render(request, 'checkout/confirmation.html', context)

def paymentCancel(request):
    context = {
        'payment_status':'cancel',
    }

    return render(request, 'checkout/confirmation.html', context)


# endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
# @csrf_exempt
# def my_webhook_view(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except ValueError:
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError:
#         return HttpResponse(status=400)
    
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         if session.payment_status == 'paid':
#             line_item = session.list_line_items(session.id, limit=1).data[0]
#             order_id = line_item['description']
#             fulfill_order(order_id)

#     return HttpResponse(status=200)

# def fulfill_order(order_id):
#     order = get_object_or_404(Order,orderId = order_id)
#     order.ordered = True
#     order.created = datetime.datetime.now()
#     order.save()
#     print('fulfilling order')