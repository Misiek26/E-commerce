from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from products.models import Category, Product
from users.forms.CustomUserCrationForm import CustomUserCreationForm
from django.contrib.auth.models import User
from .models import ClientProfile

# Create your views here.
def register_view(request):
    categories = Category.objects.all().order_by('name')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("valid")
            login(request, form.save())
            return redirect("posts:list")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    context = {
        "form" : form,
        "categories" : categories,
    }
    return render(request, "users/register.html", context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form" : form})
    
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("posts:list")
    
def test_user(request):
    users = ClientProfile.objects.all()

    return render(request, "users/test.html", {"users" : users})