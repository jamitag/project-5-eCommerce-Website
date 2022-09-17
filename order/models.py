from django.db import models

from products.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart"
    )
    item = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # Item to be put in cart
    quantity = models.IntegerField(default=1)  # Number of items to be ordered
    purchased = models.BooleanField(
        default=False
    )  # If cart items are purchased, itmes will be removed from cart
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} X {self.item}"

    # Total price of an individual item

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, "0.2f")
        return float_total


"""
Order model
"""


class Order(models.Model):
    orderItems = models.ManyToManyField(
        Cart
    )  # An order can contain several items as well as mutiple of those items
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(
        default=False
    )  # Checks order has been complete
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(
        max_length=264, blank=True, null=True
    )  # Assigns an order a transaction id
    orderId = models.CharField(max_length=200, blank=True, null=True)

    """
    Total price of all products
    """

    def get_totals(self):
        total = 0
        for order_item in self.orderItems.all():
            total += float(order_item.get_total())
        return total
