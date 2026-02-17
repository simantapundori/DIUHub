from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# This form is used to register new users
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
