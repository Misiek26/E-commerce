from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404, render
from users.models import ClientProfile
from payments.forms.BillingDetailsForm import BillingDetailsForm
from products.models import Category, Product
from django.db.models import Count
from .models import Cart, CartItem, Order, OrderItem
import json

# Create your views here.
def cart_detail(request):
    categories = Category.objects.all().order_by('name').annotate(product_count=Count('products'))

    cart = Cart(request)

    cart_price = cart.get_cart_price()
    is_anymous = request.user.is_anonymous

    if request.user is not None and not is_anymous:
        cart = CartItem.objects.filter(user=request.user)
        base_fee = 12.99
        cart_price = 0
        for item in cart:
            cart_price += item.total_price 
        
        cart_price = base_fee + float(cart_price)

    context = {
        'categories' : categories,
        'cart' : cart,
        'cart_price' : cart_price,
    }

    return render(request, 'carts/cart_detail.html', context)

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    is_anymous = request.user.is_anonymous

    if request.user is not None and not is_anymous:
        cart_item_in_database = None

        if CartItem.objects.filter(user=request.user, product__id=product_id):
            cart_item_in_database = CartItem.objects.get(user=request.user, product__id=product_id)

        if cart_item_in_database:
            cart_item_in_database.quantity+=1
            cart_item_in_database.save()
        else:
            cart_item = CartItem(user = request.user, product=product, quantity=1)
            cart_item.save()
    else:
        cart.add(product_id)
        cart.save()

    return redirect('payments:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    is_anymous = request.user.is_anonymous

    if request.user is not None and not is_anymous:
        cart_item_in_database = None

        cart_item_in_database = CartItem.objects.filter(user=request.user, product__id=product_id)
        if cart_item_in_database is not None:
            cart_item_in_database.delete()
    else:
        cart.remove(product_id=product_id)

    return redirect('payments:cart_detail')

def item_quantity_update(request, product_id, quantity):
    cart = Cart(request)
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
        cart_item_in_database = None

        if CartItem.objects.filter(user=request.user, product__id=product_id):
            cart_item_in_database = CartItem.objects.get(user=request.user, product__id=product_id)

        if cart_item_in_database:
            cart_item_in_database.quantity = quantity
            cart_item_in_database.save()
            total_price = cart_item_in_database.total_price

        base_fee = 12.99
        cart_price = 0

        for item in CartItem.objects.filter(user=request.user):
            cart_price += item.total_price

        cart_price = base_fee + float(cart_price)

    else:
        cart.update(product_id, quantity)
        cart.save()
        total_price = cart.get_total_price(product_id)
        cart_price = cart.get_cart_price()
    
    return JsonResponse({'price': total_price, 'cart_price': cart_price})

def order(request):
    categories = Category.objects.all().order_by('name').annotate(product_count=Count('products'))
    cart = Cart(request)

    cart_price = cart.get_cart_price()
    is_anymous = request.user.is_anonymous

    if request.method == 'POST':
        form = BillingDetailsForm(request.POST)
        if form.is_valid():
            return redirect("payments:summary")
    else:
        form = BillingDetailsForm()

        if request.user is not None and not is_anymous:
            cart = CartItem.objects.filter(user=request.user)
            cart_price = 0
            base_fee = 12.99
            for item in cart:
                cart_price += item.total_price 
            
            cart_price = base_fee + float(cart_price)
            user = request.user
            user_id = user.id

            try:
                user_profile = ClientProfile.objects.get(user_id=user_id)
            except:
                raise Exception("Podany użytkownik nie istnieje")
            
            form = BillingDetailsForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user_profile.address,
                'city': user_profile.city,
                'zip_code': user_profile.zip_code,
                'phone': user_profile.phone,
            })

    context = {
        'categories' : categories,
        'cart' : cart,
        'cart_price' : cart_price,
        'form' : form,
    }

    return render(request, 'carts/order.html', context)

def summary(request):
    categories = Category.objects.all().order_by('name').annotate(product_count=Count('products'))

    form = request.POST

    items=[]

    for key, value in form.items():
        if key.startswith('item-'):
            item_id = key.split('-')[1]
            count = value.split('-')[1]
            item = Product.objects.filter(id=item_id)

            price = 0.0
            for product in item:
                price = product.price * int(count)
                
            items.append({'item': item, 'count': count, 'price': price})

    context = {
        'categories' : categories,
        'form' : form,
        'items': items,
    }

    return render(request, 'carts/summary.html', context)

def confirm_order(request):
    form = request.POST
    print(form)
    user = request.user if request.user.is_authenticated else None

    order = Order.objects.create(
        user = user,

        guest_first_name = form.get('first_name'),
        guest_last_name = form.get('last_name'),
        guest_email = form.get('email'),
        guest_address = form.get('address'),
        guest_city = form.get('city'),
        guest_zip_code = form.get('zip_code'),
        guest_phone = form.get('phone'),
        guest_message = form.get('message'),

        billing_method = form.get('billing_method'),
        shipping_method = form.get('shipping_method'),

        status = 'ORDERED',

        total_amount = form.get('total_price')
    )

    for key in form:
        if key.startswith('item-'):
            item_id = key.split('-')[1]
            item_count = request.POST.get(key)
            product_obj = get_object_or_404(Product, id=item_id)
            product_price = product_obj.price * Decimal(item_count)
            ordered_item = OrderItem.objects.create(
                product = product_obj, 
                quantity = item_count, 
                price = product_price
            )
            order.order_items.add(ordered_item)

    order.save()

    # items=[]

    # for key, value in form.items():
    #     if key.startswith('item-'):
    #         item_id = key.split('-')[1]
    #         count = value.split('-')[1]
    #         item = Product.objects.filter(id=item_id)

    #         price = 0.0
    #         for product in item:
    #             price = product.price * int(count)
                
    #         items.append({'item': item, 'count': count, 'price': price})

    context = {
        'form' : form,
        # 'items': items,
    }

    return render(request, 'carts/summary.html', context)