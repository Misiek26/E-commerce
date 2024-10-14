from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name="list"),
    path('<int:p>/', views.products_list, name="list"),
    # path('new-post/', views.post_new, name="new-post"),
    path('<slug:slug>', views.product_page, name="page"),
]