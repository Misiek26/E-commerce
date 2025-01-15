from django.db import models
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity}
        self.save()

    def update(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        self.save()

    def get_total_price(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            product = Product.objects.get(id = product_id)
            item = self.cart[product_id]
            total_price = item['quantity'] * product.price
            return total_price
        
    def get_cart_price(self):
        cart_price = 0
        base_fee = 12.99

        for item in self.cart:
            cart_price += self.get_total_price(item)

        cart_price = float(cart_price)

        return round(cart_price + base_fee, 2)

    def save(self):
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def clear(self):
        del self.session['cart']
        self.save()
    
    def show_item_quantities(self):
        quantities = {}
        for product_id, details in self.cart.items():
            quantities[product_id] = details['quantity']
        return quantities
    
# Order model
class Order(models.Model):
    STATUS_CHOICES = [
        ('ORDERED', 'Zamówione'),
        ('PAID', 'Opłacone'),
        ('PREPARING', 'W trakcie przygotowania'),
        ('COMPLETED', 'Zakończone'),
        ('CANCELLED', 'Anulowane'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ORDERED')
    payment_method = models.CharField(max_length=25, null=False, blank=False)
    shipping_method = models.CharField(max_length=15, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Zamówienie #{self.id} - {self.user.username} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)