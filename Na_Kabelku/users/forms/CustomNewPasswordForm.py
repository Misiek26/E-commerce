from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import SetPasswordForm

class CustomNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Hasło",
        error_messages={'required': 'Proszę wprowadzić hasło.'},
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Hasło',
            'class': 'input',
            'id': 'new-password1-input'
        }
        ),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})',
                message="Hasło powinno zawierać minimum 8 znaków, w tym 1 dużą literę, 1 cyfrę i 1 znak specjalny.",
            )

        ]
    )

    new_password2 = forms.CharField(
        label="Powtórz hasło",
        error_messages={
            'required': 'Proszę powtórzyć hasło',
            'password_mismatch': 'Hasła muszą być takie same.',
            },
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Powtórz hasło',
            'class': 'input',
            'id': 'new-password2-input'
        }
        ),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})',
                message="Hasła muszą być takie same.",
            )

        ]
    )