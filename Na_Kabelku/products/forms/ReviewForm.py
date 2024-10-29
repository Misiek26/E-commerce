from django import forms
from ..models import Review
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'placeholder': 'Dodaj swoją opinię tutaj...'}),
        }

        error_messages = {
            'rating': {
                'required': 'Proszę podać ocenę od 1 do 5.',
                'invalid': 'Zaznacz prawidłowo ocenę.',
            },
            'comment': {
                'required': 'Komentarz jest wymagany.',
            },
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        
        if not self.user or not self.user.is_authenticated:
            raise ValidationError("Musisz być zalogowany, aby dodać opinię.")

        return cleaned_data