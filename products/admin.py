from django.contrib import admin
from .models import Product, Category


"""
Show item details within admin panel
"""


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "category",
        "price",
    )

    ordering = ("sku",)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
