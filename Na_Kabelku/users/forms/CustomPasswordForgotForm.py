from django import forms
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordForgotForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Wprowadź swój adres email',
            'class': 'input',
            'id': 'email-input'
        }),
        label="Adres email",
        error_messages={
            'required': 'Proszę wprowadzić swój adres email.',
            'invalid': 'Nieprawidłowy email. Wprowadź poprawne dane.'
        }
    )