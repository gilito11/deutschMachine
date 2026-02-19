from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    target_country = forms.ChoiceField(choices=UserProfile.COUNTRY_CHOICES)
    target_languages = forms.MultipleChoiceField(
        choices=[('en', 'English'), ('de', 'German')],
        widget=forms.CheckboxSelectMultiple,
    )
    current_level_en = forms.ChoiceField(
        choices=[('', '---')] + list(dict.fromkeys([
            ('A1', 'A1 - Beginner'), ('A2', 'A2 - Elementary'),
            ('B1', 'B1 - Intermediate'), ('B2', 'B2 - Upper Intermediate'),
        ])),
        required=False,
    )
    current_level_de = forms.ChoiceField(
        choices=[('', '---')] + list(dict.fromkeys([
            ('A1', 'A1 - Beginner'), ('A2', 'A2 - Elementary'),
            ('B1', 'B1 - Intermediate'), ('B2', 'B2 - Upper Intermediate'),
        ])),
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
