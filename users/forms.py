from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'input-field'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email address',
                'class': 'input-field'
            }),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'input-field'
        }),
        help_text=""
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'input-field'
        }),
        help_text=""
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"   # force student role
        if commit:
            user.save()
        return user