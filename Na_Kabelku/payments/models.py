from django.db import models
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.
class ChartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
class Chart:
    def __init__(self, request):
        self.session = request.session
        chart = self.session.get('chart')
        if 'chart' not in request.session:
            chart = self.session['chart'] = {}
        self.chart = chart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.chart:
            self.chart[product_id]['quantity'] += quantity
        else:
            self.chart[product_id] = {'quantity': quantity}
        self.save()

    def update(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.chart:
            self.chart[product_id]['quantity'] = quantity
        self.save()

    def get_total_price(self, product_id):
        product_id = str(product_id)
        if product_id in self.chart:
            product = Product.objects.get(id = product_id)
            item = self.chart[product_id]
            total_price = item['quantity'] * product.price
            return total_price
        
    def get_cart_price(self):
        cart_price = 0
        for item in self.chart:
            cart_price += self.get_total_price(item)
        return cart_price

    def save(self):
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.chart:
            del self.chart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.chart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.chart[str(product.id)]['product'] = product

        for item in self.chart.values():
            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def clear(self):
        del self.session['chart']
        self.save()
    
    def show_item_quantities(self):
        quantities = {}
        for product_id, details in self.chart.items():
            quantities[product_id] = details['quantity']
        return quantities