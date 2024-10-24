from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activation/link/<int:user_id>/', views.activate_link, name="activate-link"),
    path('password/forgot/', views.forgot_password_view, name="forgot-password"),
    path('logout/', views.logout_view, name="logout"),
]