import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        label=("Nazwa użytkownika lub Email"),
        widget=forms.TextInput(
        attrs={
            'placeholder': 'Nazwa użytkownika lub Email',
            'class': 'input',
            'id': 'username-input'
        }
        ),
        error_messages={
            'required': 'Nazwa użytkownika lub email jest wymagana.',
        }
    )

    password = forms.CharField(
        label="Hasło",
        error_messages={'required': 'Proszę wprowadzić hasło.'},
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Hasło',
            'class': 'input',
            'id': 'password-input'
        }
        ),
    )
