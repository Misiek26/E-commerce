from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password/forgot/activate/<uidb64>/<token>/', views.forgot_activate, name='forgot-activate'),
    path('activation/link/<int:user_id>/', views.activate_link, name="activate-link"),
    path('password/forgot/activation/link/<int:user_id>/', views.forgot_activate_link, name="forgot-activate-link"),
    path('password/forgot/', views.forgot_password_view, name="forgot-password"),
    path('password/new/', views.set_new_password, name="set-password"),
    path('logout/', views.logout_view, name="logout"),
]