from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404, render
from products.models import Category, Product
from django.db.models import Count
from .models import Chart, ChartItem
import json

# Create your views here.
def chart_detail(request):
    categories = Category.objects.all().order_by('name').annotate(product_count=Count('products'))

    chart = Chart(request)
    cart_price = chart.get_cart_price()
    is_anymous = request.user.is_anonymous

    if request.user is not None and not is_anymous:
        chart = ChartItem.objects.filter(user=request.user)

    context = {
        'categories' : categories,
        'chart' : chart,
        'cart_price' : cart_price,
    }

    return render(request, 'charts/chart_detail.html', context)

def chart_add(request, product_id):
    chart = Chart(request)
    product = get_object_or_404(Product, id=product_id)
    is_anymous = request.user.is_anonymous

    if request.user is not None and not is_anymous:
        chart_item_in_database = None

        if ChartItem.objects.filter(user=request.user, product__id=product_id):
            chart_item_in_database = ChartItem.objects.get(user=request.user, product__id=product_id)

        if chart_item_in_database:
            chart_item_in_database.quantity+=1
            chart_item_in_database.save()
        else:
            chart_item = ChartItem(user = request.user, product=product, quantity=1)
            chart_item.save()
    else:
        chart.add(product_id)
        chart.save()

    return redirect('payments:chart_detail')

def chart_remove(request, product_id):
    chart = Chart(request)
    is_anymous = request.user.is_anonymous

    if request.user is not None and not is_anymous:
        chart_item_in_database = None

        chart_item_in_database = ChartItem.objects.filter(user=request.user, product__id=product_id)
        if chart_item_in_database is not None:
            chart_item_in_database.delete()
    else:
        chart.remove(product_id=product_id)

    return redirect('payments:chart_detail')

def item_quantity_update(request, product_id, quantity):
    chart = Chart(request)
    product = get_object_or_404(Product, id=product_id)
    is_anymous = request.user.is_anonymous
    item = None

    max_quantity = product.quantity
    if quantity > max_quantity:
        quantity = max_quantity
    elif quantity < 0:
        quantity = 0
    else:
        quantity = quantity

    if request.user is not None and not is_anymous:
        chart_item_in_database = None

        if ChartItem.objects.filter(user=request.user, product__id=product_id):
            chart_item_in_database = ChartItem.objects.get(user=request.user, product__id=product_id)

        if chart_item_in_database:
            chart_item_in_database.quantity = quantity
            chart_item_in_database.save()
            total_price = chart_item_in_database.total_price
    else:
        chart.update(product_id, quantity)
        chart.save()
        total_price = chart.get_total_price(product_id)

    cart_price = chart.get_cart_price()

    return JsonResponse({'price': total_price, 'cart_price': cart_price})
