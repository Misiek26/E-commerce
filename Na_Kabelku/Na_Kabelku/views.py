from django.shortcuts import render
from products.models import Category, Product

def homepage(request):
    categories = Category.objects.all().order_by('name')
    categories_home = Category.objects.all()[:3]
    new_products = Product.objects.all().order_by('-created_date')[:8]
    top_products = Product.objects.all().order_by('-sold_quantity')[:8]

    context = {
        'categories' : categories,
        'categories_home' : categories_home,
        'new_products' : new_products,
        'top_products' : top_products,
        'top_products_category': {
            category: Product.objects.filter(category=category).order_by('-sold_quantity')[:6] 
            for category in categories_home
        }
    }

    return render(request, 'home.html', context)
