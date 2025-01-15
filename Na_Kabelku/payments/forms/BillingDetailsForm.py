from django import forms

class BillingDetailsForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        label="Imię",
        widget=forms.TextInput(attrs={
            'class': 'input first-name',
            'placeholder': 'Imię',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        label="Nazwisko",
        widget=forms.TextInput(attrs={
            'class': 'input last-name',
            'placeholder': 'Nazwisko',
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'Email',
        })
    )
    address = forms.CharField(
        max_length=255,
        label="Adres",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Adres',
        })
    )
    city = forms.CharField(
        max_length=100,
        label="Miasto",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Miasto',
        })
    )
    zip_code = forms.CharField(
        max_length=20,
        label="Kod pocztowy",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'pattern': r'^\d{2}-\d{3}$',
            'title': 'Wprowadź kod pocztowy w formacie 12-345',
            'placeholder': 'Kod pocztowy',
        })
    )
    phone = forms.CharField(
        max_length=9,
        label="Telefon",
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'class': 'input',
            'pattern': '[0-9]{9}',
            'title': 'Wprowadź 9-cyfrowy numer telefonu',
            'placeholder': 'Telefon',
        })
    )
    message = forms.CharField(
        label="Wiadomość do sprzedającego",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'input',
            'placeholder': 'Napisz wiadomość',
        })
    )
    create_account = forms.BooleanField(
        required=False,
        label="Utwórz konto",
        widget=forms.CheckboxInput(attrs={
            'id': 'create-account'
        })
    )

    SHIPPING_METHODS = {
        'inpost': {'label': 'Paczkomat Inpost', 'price': '12.99'},
        'kurier': {'label': 'Kurier DPD', 'price': '17.99'},
        'pobranie': {'label': 'Kurier za pobraniem', 'price': '19.99'},
    }
    
    shipping_method = forms.ChoiceField(
        label="Metody Dostawy",
        required=True,
        choices=[
            ('inpost', 'Paczkomat Inpost (12.99zł)'),
            ('kurier', 'Kurier DPD (17.99zł)'),
            ('pobranie', 'Kurier za pobraniem (19.99zł)')
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'shipping-method',
            'title': 'Wybierz metodę dostawy',
        }),
        error_messages={'required': 'Wybierz metodę dostawy.'}
    )
    billing_method = forms.ChoiceField(
        label="Metody Płatności",
        required=True,
        choices=[
            ('przelew', 'Przelew online'),
            ('BLIK', 'BLIK'),
            ('pobranie', 'Płatność przy odbiorze')
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'billing-method'
        }),
        error_messages={'required': 'Wybierz metodę płatności.'}
    )
