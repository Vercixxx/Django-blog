from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Not required, used for password recovery")
    
    username = forms.CharField(min_length=5)
    password1 = forms.CharField(help_text="At least 8 characters", min_length=8, label="Password")
    password2 = forms.CharField(label="Repeat password")
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]