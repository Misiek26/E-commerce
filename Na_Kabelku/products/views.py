from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category, Brand, Review
from products.forms.ReviewForm import ReviewForm
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
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

    related_products = Product.objects.filter(category = product.category).exclude(slug=slug)

    reviews = Review.objects.filter(product = product).order_by('-created_at')
    reviews_count = reviews.count()

    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating_stars = round(average_rating)
    average_rating = round(average_rating, 1)
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in reviews:
        rating_counts[review.rating] += 1

    rating_counts_percentage = [
        (rating_counts[star] / reviews_count) * 100 if reviews_count > 0 else 0
        for star in range(1, 6)
    ]

    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page', p)
    page_obj = paginator.page(page_number)  

    context = {
        'product' : product,
        'categories' : categories,
        'related_products' : related_products,
        'reviews' : page_obj,
        'reviews_count' : reviews_count,
        'average_rating' : average_rating,
        'average_rating_stars' : average_rating_stars,
        'rating_counts': rating_counts,
        'rating_counts_percentage' : rating_counts_percentage,
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
    reviews_count = reviews.count()

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
        'reviews_count' : reviews_count,
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

def search_view(request, p=1):
    path = request.path
    path_matches_query = bool(re.match(r'^/products/search/list/.*$', path))
    path_matches_paginator = bool(re.match(r'^/products/search/list/[0-9]+/.*$', path))

    if path_matches_paginator:
        path_paginator = '/' + '/'.join(path.strip('/').split('/')[:-1]) + '/'
    else:
        path_paginator = request.path

    categories = Category.objects.all().order_by('name').annotate(product_count=Count('products'))
    brands = Brand.objects.all().order_by('name').annotate(product_count=Count('products'))
    
    category_query_name = request.GET.get('category_query', '')

    category_id = None

    if category_query_name != "all":
        category_id = Category.objects.get(name=category_query_name).id

    sort_by = request.GET.get('sort_by', '-created_date')
    min_price = float(request.GET.get('min-price', '1.00'))
    max_price = float(request.GET.get('max-price', '9999.00'))
    selected_brands = request.GET.getlist('brand')
    selected_brands = [int(brands) for brands in selected_brands]
    selected_categories = request.GET.getlist('category') 
    selected_categories = [int(cat) for cat in selected_categories]

    product_filter = Product.objects.filter(price__range=(min_price, max_price))

    query = ''

    if 'query' in request.GET:
        query = request.GET.get('query', '')
        product_filter = Product.objects.filter(title__icontains=query, price__range=(min_price, max_price))
        if category_id:
            product_filter = product_filter.filter(category=category_id)
    
    if selected_categories:
        product_filter = product_filter.filter(category__in=selected_categories)

    if selected_brands:
        product_filter = product_filter.filter(brand__in=selected_brands)

    products = product_filter.order_by(sort_by)
    
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page', p)
    page_obj = paginator.page(page_number)

    context = {
        'path_matches_query' : path_matches_query,
        'products' : page_obj, 
        'categories' : categories, 
        'brands' : brands,
        'selected_categories' : selected_categories,
        'selected_brands' : selected_brands,
        'path_paginator' : path_paginator,
        'query' : query,
        'category_query_name' : category_query_name,
    }

    return render(request, 'products/products_list.html', context)