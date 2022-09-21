from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_products, name="products"),
    path("<product_id>", views.product_detail, name="product_detail"),
    path("<int:pk>/add-comment", views.add_comment, name="add_comment"),
    path("<int:pk>/delete-comment", views.delete_comment, name="del_comment"),
]
