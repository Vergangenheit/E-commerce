from typing import Dict

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_detail(request: HttpRequest, slug: str) -> HttpResponse:
    product: Product = get_object_or_404(Product, slug=slug, in_stock=True)

    return render(request, 'store/products/single.html', {'product': product})


# Create your views here.
def product_all(request: HttpRequest) -> HttpResponse:
    # grab the data
    products: QuerySet = Product.products.all()
    # make that data available on my template
    return render(request, 'store/home.html', {'products': products})


def category_list(request: HttpRequest, category_slug: str) -> HttpResponse:
    category: Category = get_object_or_404(Category, slug=category_slug)
    products: QuerySet = Product.objects.filter(category=category)

    return render(request, 'store/products/category.html', {'category': category, 'products': products})
