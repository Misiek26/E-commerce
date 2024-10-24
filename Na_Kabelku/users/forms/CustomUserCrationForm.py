from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..models import ClientProfile

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True, 
        max_length=50, 
        label="Nazwa użytkownika", 
        error_messages={
            'required': 'Nazwa użytkownika jest wymagana.',
            'max_length': 'Nazwa użytkownika nie może przekraczać 50 znaków.',
            'unique': 'Ten użytkownik już istnieje, proszę wybrać inną nazwę.',
            'invalid': 'Nazwa użytkownika zawiera niedozwolone znaki.'
            },
        widget=forms.TextInput(
        attrs={
            'placeholder': 'Nazwa użytkownika',
            'class': 'input',
            'id': 'username-input'
        }
        ),
    )

    email = forms.EmailField(
        required=True,
        label="Email", 
        error_messages={
            'required': 'Proszę wprowadzić poprawny adres email.',
            'invalid': 'Proszę wprowadzić poprawny adres email.',
            'unique': 'Ten email jest już zajęty.',
            },
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'class': 'input',
                'id': 'email-input',
            }
        ),
    )

    first_name = forms.CharField(
        required=True,
        max_length=30,
        label="Imię",
        error_messages={'required': 'Proszę wprowadzić imię.'},
        widget=forms.TextInput(
        attrs={
            'placeholder': 'Imię',
            'class': 'input',
            'id': 'firstname-input'
        }
        ),
    )

    last_name = forms.CharField(
        required=True,
        max_length=30,
        label="Nazwisko",
        error_messages={'required': 'Proszę wprowadzić nazwisko.'},
        widget=forms.TextInput(
        attrs={
            'placeholder': 'Nazwisko',
            'class': 'input',
            'id': 'lastname-input'
        }
        ),
    )

    password1 = forms.CharField(
        label="Hasło",
        error_messages={'required': 'Proszę wprowadzić hasło.'},
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Hasło',
            'class': 'input',
            'id': 'password1-input'
        }
        ),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})',
                message="Hasło powinno zawierać minimum 8 znaków, w tym 1 dużą literę, 1 cyfrę i 1 znak specjalny.",
            )

        ]
    )

    password2 = forms.CharField(
        label="Powtórz hasło",
        error_messages={
            'required': 'Proszę powtórzyć hasło',
            'password_mismatch': 'Hasła muszą być takie same.',
            },
        widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Powtórz hasło',
            'class': 'input',
            'id': 'password2-input'
        }
        ),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{8,})',
                message="Hasła muszą być takie same.",
            )

        ]
    )

    phone = forms.CharField(
        required=True,
        max_length=9,
        label="Numer telefonu",
        widget=forms.TextInput(
        attrs={
            'type': 'tel',
            'placeholder': 'Numer telefonu',
            'class': 'input',
            'id': 'phone-input',
            'pattern': '[0-9]{9}',
            'title': 'Wprowadź numer telefonu w formacie 123456789',
            'unique': True,
        }
        ),
        error_messages={
            'required': 'Wprowadź poprawny numer telefonu.',
            'invalid': 'Wprowadź poprawny numer telefonu.',
            'unique': 'Podany numer jest już zajęty.'
            },
        
    )

    address = forms.CharField(
        required=True,
        label="Adres",
        widget=forms.Textarea(
        attrs={
            'placeholder': 'Ulica i numer domu/mieszkania',
            'class': 'input',
            'rows': 3,
            'id': 'address-input',
        }
        ),
        max_length=300,
        error_messages={'required': 'Proszę wprowadzić poprawny adres.'}
    )

    zip_code = forms.CharField(
        required=True,
        max_length=6,
        label="Kod pocztowy",
        widget=forms.TextInput(
        attrs={
            'placeholder': 'Kod pocztowy',
            'class': 'input',
            'id': 'zip-code-input',
            'pattern': r'^\d{2}-\d{3}$',
            'title': 'Wprowadź kod pocztowy w formacie 12-345',
        }
        ),
    )
    city = forms.CharField(
        required=True,
        max_length=30,
        label="Miasto",
        widget=forms.TextInput(
        attrs={
            'placeholder': 'Miasto',
            'class': 'input',
            'id': 'city-input',
        }
        ),
    )

    rodo = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(
        attrs={
            'class': 'input',
            'id': 'rodo-input',
        }
        ),
        error_messages={'required': 'Musisz wyrazić zgodę na przetwarzanie danych osobowych.'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'address', 'zip_code', 'city', 'password1', 'password2', 'rodo')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            ClientProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                zip_code=self.cleaned_data['zip_code'],
                rodo=True
            )

        return user
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Hasła muszą być takie same.",
                code='password_mismatch',
            )
        return password2
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if ClientProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                "Podany numer telefonu jest już zajęty.",
                code='unique',
            )
        
        return phone