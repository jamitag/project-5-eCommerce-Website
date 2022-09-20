from django.shortcuts import render, get_object_or_404, redirect

# authentications
from django.contrib.auth.decorators import login_required

# model
from .models import Cart, Order
from products.models import Product

# messages
from django.contrib import messages

# Create your views here.

"""
Calls items to cart which havent been purchased
"""


@login_required
def add_to_cart(request, pk):
    # call the item we want to add to cart
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(
        item=item, user=request.user, purchased=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(
            item=item
        ).exists():  # increase an item quantity in your cart
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "The number of items has been updated")
            return redirect("/")
        else:
            order.orderItems.add(order_item[0])
            messages.info(request, "Item added to cart")
            return redirect("/")

    else:
        order = Order(user=request.user)
        order.save()
        order.orderItems.add(order_item[0])
        messages.info(request, "Item added to cart")
        return redirect("/")


"""
View all cart items
"""


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(
            request, "order/cart.html",
            context={"carts": carts, "order": order}
        )
    else:
        messages.warning(request, "No items in your cart")
        return redirect("/")


"""
Removes items for cart
"""


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False
            )
            order_item = order_item[0]
            order.orderItems.remove(order_item)
            order_item.delete()
            messages.warning(request, "Item removed from cart")
            return redirect("cart")
        else:
            messages.info(request, "Item is not in cart")
            return redirect("home")
    else:
        messages.info(request, "No active order")
        return redirect("home")


"""
Increase an item already in our cart
"""


@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False
            )
            order_item = order_item[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} added")
                return redirect("cart")

        else:
            messages.info(request, f"{item.name} is not in cart")
            return redirect("cart")

    else:
        messages.info(request, "No active order")
        return redirect("home")


"""
Decrease an item already in our cart
"""


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False
            )
            order_item = order_item[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} removed")
                return redirect("cart")
            else:
                order.orderItems.remove(order_item)
                order_item.delete()
                messages.warning(request,
                                 f"{item.name} removed from your cart")
                return redirect("cart")

        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect("home")

    else:
        messages.info(request, "No active order")
        return redirect("home")
