from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, ProductComment
from .forms import CommentForm
from datetime import datetime

# Create your views here.


def all_products(request):
    """Show all products"""

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            queries = Q(name__icontains=query) | Q(desc__icontains=query)
            products = products.filter(queries)

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """Show individual products"""

    product = get_object_or_404(Product, pk=product_id)

    num_comments = ProductComment.objects.filter(product=product).count()

    context = {
        "product": product,
        "num_comments": num_comments,
    }

    return render(request, "products/product_detail.html", context)


def add_comment(request, pk):
    product = Product.objects.get(id=pk)
    form = CommentForm(instance=product)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=product)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['body']
            cmnt = ProductComment(product=product, author=name, body=body,
                                  created=datetime.now())
            cmnt.save()
            return redirect('home')
        else:
            print('form is invalid')
    else:
        form = CommentForm()
    context = {
        'form': form,
    }

    return render(request, 'products/add_comment.html', context)


def delete_comment(request, pk):
    product = Product.objects.get(id=pk)
    comment = ProductComment.objects.filter(product=pk).last()
    product_id = comment.product.id
    comment.delete()
    return redirect('home')
