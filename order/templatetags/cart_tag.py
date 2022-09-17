from atexit import register
from django import template
from order.models import Order

register = template.Library()

"""
Adds the number of items within cart to icon in navbar
"""


@register.filter
def cart_total(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].orderItems.count()
    else:
        return 0
