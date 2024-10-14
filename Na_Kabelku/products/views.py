from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category, Brand
from django.db.models import Count

# Create your views here.
def products_list(request, p=1):
    categories = Category.objects.all().order_by('name').annotate(product_count=Count('products'))
    brands = Brand.objects.all().order_by('name').annotate(product_count=Count('products'))

    sort_by = request.GET.get('sort_by', '-created_date')
    min_price = float(request.GET.get('min-price', '1.00'))
    max_price = float(request.GET.get('max-price', '9999.00'))
    selected_brands = request.GET.getlist('brand')
    selected_brands = [int(brands) for brands in selected_brands]
    selected_categories = request.GET.getlist('category') 
    selected_categories = [int(cat) for cat in selected_categories]

    product_filter = Product.objects.filter(price__range=(min_price, max_price))
    
    if selected_categories:
        product_filter = product_filter.filter(category__in=selected_categories)

    if selected_brands:
        product_filter = product_filter.filter(brand__in=selected_brands)

    products = product_filter.order_by(sort_by)
    
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page', p)
    page_obj = paginator.page(page_number)

    context = {
        'products' : page_obj, 
        'categories' : categories, 
        'brands' : brands,
        'selected_categories' : selected_categories,
        'selected_brands' : selected_brands
    }

    return render(request, 'products/products_list.html', context)

def product_page(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', {'product' : product})