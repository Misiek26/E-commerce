from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category, Brand, Review
from products.forms.ReviewForm import ReviewForm
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

# Create your views here.
def products_list(request, p=1):
    path = request.path
    path_matches = bool(re.match(r'^/products/[a-z]+/.*$', path))
    path_matches_paginator = bool(re.match(r'^/products/[0-9]+/.*$', path))

    if path_matches_paginator:
        path_paginator = '/' + '/'.join(path.strip('/').split('/')[:-1]) + '/'
    else:
        path_paginator = request.path

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
        'path_matches' : path_matches,
        'products' : page_obj, 
        'categories' : categories, 
        'brands' : brands,
        'selected_categories' : selected_categories,
        'selected_brands' : selected_brands,
        'path_paginator' : path_paginator
    }

    return render(request, 'products/products_list.html', context)

def products_list_category(request, category, p=1):
    path = request.path
    path_matches = bool(re.match(r'^/products/[a-z]+/.*$', path))
    path_matches_paginator = bool(re.match(r'^/products/[a-z]+/[0-9]+/.*$', path))

    if path_matches_paginator:
        path_paginator = '/' + '/'.join(path.strip('/').split('/')[:-1]) + '/'
    else:
        path_paginator = request.path


    categories = Category.objects.all().order_by('name')
    category_id = Category.objects.get(slug = category).id

    path_category = path.strip('/').split('/')[1]
    brands = Brand.objects.filter(products__category = category_id).order_by('name').annotate(product_count=Count('products'))
    
    sort_by = request.GET.get('sort_by', '-created_date')
    min_price = float(request.GET.get('min-price', '1.00'))
    max_price = float(request.GET.get('max-price', '9999.00'))
    selected_brands = request.GET.getlist('brand')
    selected_brands = [int(brands) for brands in selected_brands]

    product_filter = Product.objects.filter(price__range=(min_price, max_price))
    product_filter = product_filter.filter(category=category_id)

    if selected_brands:
        product_filter = product_filter.filter(brand__in=selected_brands)

    products = product_filter.order_by(sort_by)
    
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page', p)
    page_obj = paginator.page(page_number)

    context = {
        'path_matches' : path_matches,
        'products' : page_obj, 
        'brands' : brands,
        'categories' : categories,
        'selected_brands' : selected_brands,
        'path_paginator' : path_paginator,
        'path_category' : path_category
    }

    return render(request, 'products/products_list.html', context)

def product_page(request, slug, p=1):
    product = Product.objects.get(slug=slug)
    categories = Category.objects.all().order_by('name')
    reviews = Review.objects.filter(product = product).order_by('-created_at')

    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page', p)
    page_obj = paginator.page(page_number)  

    context = {
        'product' : product,
        'categories' : categories,
        'reviews' : page_obj,
        'stars_range' : range(1,6),
        'has_next': page_obj.has_next(),
    }
    return render(request, 'products/product_page.html', context)

def load_reviews(request, slug, p=2):
    product = Product.objects.get(slug=slug)
    reviews = Review.objects.filter(product = product).order_by('-created_at')
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page', p)
    page_obj = paginator.page(page_number)  

    reviews_data = []
    for review in page_obj:
        reviews_data.append({
            'username': review.user.username,
            'comment': review.comment,
            'rating': review.rating,
            'created_at': review.created_at.strftime('%d.%m.%Y')
        })

    context ={
        'reviews_list' : reviews_data,
        'has_next': page_obj.has_next(),
    }
    
    return JsonResponse(context, safe=False)

def add_review(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            form.add_error("rating", "Dziękujemy za dodanie opinii.")
            review.user = request.user
            review.product = product
            review.save()
            return JsonResponse({
                'success': True,
                'username': review.user.username,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.strftime('%d.%m.%Y')
            })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)