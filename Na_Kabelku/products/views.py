from django.shortcuts import render
from .models import Product

# Create your views here.
def products_list(request):
    products = Product.objects.all().order_by('-created_date')
    return render(request, 'products/products_list.html', {'products' : products})

def product_page(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', {'product' : product})