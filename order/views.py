from django.shortcuts import render, get_object_or_404, redirect
# authentications 
from django.contrib.auth.decorators import login_required

# model
from .models import Cart, Order
from products.models import Product

# messages
from django.contrib import messages

# Create your views here.

@login_required

def add_to_cart(request, pk):
    # call the item we want to add to cart
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists(): 
        order = order_qs[0] 
        if order.orderItems.filter(item=item).exists(): # increase an item quantity in your cart
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, 'The number of items has been updated')
            return redirect('/')
        else:
            order.orderItems.add(order_item[0]) 
            messages.info(request, 'Item added to cart')
            return redirect('/')

    else:
        order = Order(user=request.user)
        order.save()
        order.orderItems.add(order_item[0])
        messages.info(request, 'Item added to cart')
        return redirect('/')
        
@login_required

def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'order/cart.html', context={'carts':carts, 'order':order})
    else:
        messages.warning(request, 'You don"t have any items in your cart')
        return redirect('/')
