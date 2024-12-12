from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('chart/', views.chart_detail, name="chart_detail"),
    path('chart/add/<int:product_id>/', views.chart_add, name='chart_add'),
    path('chart/remove/<int:product_id>/', views.chart_remove, name='chart_remove'),
    path('chart/item/update/<int:product_id>/<int:quantity>/', views.item_quantity_update, name='item_quantity_update'),
]