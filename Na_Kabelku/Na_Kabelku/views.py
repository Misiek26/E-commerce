from django.shortcuts import render
from products.models import Category, Product

def homepage(request):
    categories = Category.objects.all().order_by('name')
    categories_home = Category.objects.all()[:3]
    new_products = Product.objects.all().order_by('-created_date')[:8]

    context = {
        'categories' : categories,
        'categories_home' : categories_home,
        'new_products' : new_products,
    }

    return render(request, 'home.html', context)
