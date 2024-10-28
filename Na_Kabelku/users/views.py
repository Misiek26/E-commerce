from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from products.models import Category, Product
from users.forms.CustomUserCrationForm import CustomUserCreationForm
from users.forms.CustomUserLoginForm import CustomUserLoginForm
from users.forms.CustomPasswordForgotForm import CustomPasswordForgotForm
from users.forms.CustomNewPasswordForm import CustomNewPasswordForm
from django.contrib.auth.models import User
from .models import ClientProfile
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.html import strip_tags

# Create your views here.
def register_view(request):
    categories = Category.objects.all().order_by('name')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            user = User.objects.get(username = user_name)
            user.is_active = False
            user.save()
            return redirect("users:activate-link", user_id = user.id)
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    context = {
        "form" : form,
        "categories" : categories,
    }
    return render(request, "users/register.html", context)

def activate_link(request, user_id=0):
    categories = Category.objects.all().order_by('name')
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id = user_id)
        user_is_active = user.is_active
    else:
        user = None 
        user_is_active = False
    
    if user is not None and user_is_active == False:
        resend = send_activation_email(user, request)
        return render(request, "users/activate_link.html", {"categories" : categories, "resend": resend})
    elif user_is_active==True:
        return render(request, 'users/activation_valid.html', {"categories" : categories})
    else:
        return redirect('/')

def send_activation_email(user, request):
    mail_subject = 'Potwierdź aktywacje swojego konta'
    current_site = get_current_site(request)
    message = render_to_string('users/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(mail_subject, message, 'wytworniaogorek@gmail.com', [user.email], html_message=message)

def activate(request, uidb64, token):
    categories = Category.objects.all().order_by('name')
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'users/activation_valid.html')
    else:
        return render(request, 'users/activation_invalid.html', {'categories': categories} )
    
def login_view(request):
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        if "@" in request.POST['username']:
            try:
                user = User.objects.get(email = request.POST['username'])
                data_copy=request.POST.copy()
                data_copy['username'] = user.username
            except:
                User.DoesNotExist
                form = CustomUserLoginForm(data = request.POST)
                form.add_error('username', "Podany email nie istnieje.")
        else:
            data_copy =  request.POST

        form = CustomUserLoginForm(data = data_copy)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            form = CustomUserLoginForm(data = request.POST)
            form.add_error('password', 'Nieprawidłowy login lub hasło. Wprowadź poprawne dane.')
        
    else:
        form = CustomUserLoginForm()

    return render(request, "users/login.html", {"form" : form, "categories": categories})

def forgot_password_view(request):
    categories = Category.objects.all().order_by('name')

    if request.method == "POST":
        form = CustomPasswordForgotForm(data = request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email = request.POST['email'])
                if user.is_active == True:
                    return redirect('users:forgot-activate-link', user_id = user.id)
                else:
                    form.add_error('email', "Konto użytkownika przypisane do podanego emaila jest nieaktywne.")
            except:
                User.DoesNotExist
                form = CustomPasswordForgotForm(data = request.POST)
                form.add_error('email', "Podany email nie istnieje.")
        else:
            form = CustomPasswordForgotForm(data = request.POST)
    else:
        form = CustomPasswordForgotForm()

    return render(request, "users/forgot_password.html", {"form" : form, "categories": categories})

def forgot_activate_link(request, user_id=0):
    categories = Category.objects.all().order_by('name')
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id = user_id)
        user_is_active = user.is_active
    else:
        user = None 
        user_is_active = False
    
    if user is not None and user_is_active == True:
        resend = send_reset_email(user, request)
        return render(request, "users/forgot_password_link.html", {"categories" : categories, "resend": resend})
    else:
        return redirect('/users/login/')
    
def forgot_activate(request, uidb64, token):
    categories = Category.objects.all().order_by('name')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        form = CustomNewPasswordForm(user=user)
        login(request, user)
        return render(request, 'users/new_password.html', {'categories': categories, 'form': form})
    else:
        return render(request, 'users/activation_invalid.html', {'categories': categories} )

@login_required
def set_new_password(request):
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        form = CustomNewPasswordForm(user=request.user, data=request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, "Twoje hasło zostało zmienione pomyślnie")
            return redirect('/')
    else:
        form = CustomNewPasswordForm(user=request.user)
    
    return render(request, 'users/new_password.html', {'categories': categories, 'form': form})

def send_reset_email(user, request):
    mail_subject = 'Resetowanie hasła do konta'
    current_site = get_current_site(request)
    message = render_to_string('users/forgot_password_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(mail_subject, message, 'wytworniaogorek@gmail.com', [user.email], html_message=message)
    
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("posts:list")
