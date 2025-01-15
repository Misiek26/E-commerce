from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/item/update/<int:product_id>/<int:quantity>/', views.item_quantity_update, name='item_quantity_update'),
    path('order/', views.order, name="order"),
    path('summary/', views.summary, name="summary"),
]