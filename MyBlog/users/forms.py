from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=10, min_length=4, required=True)
    email = forms.EmailField(required=False, help_text="Not required, used for password recovery")
    password1 = forms.CharField(widget=forms.PasswordInput, help_text="At least 8 characters", min_length=8, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username