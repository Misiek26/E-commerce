from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name="list"),
    path('<int:p>/', views.products_list, name="list"),
    path('<str:category>/', views.products_list_category, name="list_category"),
    path('<str:category>/<int:p>/', views.products_list_category, name="list_category"),
    # path('new-post/', views.post_new, name="new-post"),
    path('product/<slug:slug>/', views.product_page, name="page"),
    path('product/<slug:slug>/<int:p>/', views.product_page, name="page"),
    path('product/<slug:slug>/load-reviews/', views.load_reviews, name='load-reviews'),
    path('product/<slug:slug>/load-reviews/<int:p>/', views.load_reviews, name='load-reviews'),
    path('product/reviews/add-review/<int:product_id>/', views.add_review, name='add-review'),
]