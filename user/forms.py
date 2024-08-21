from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from captcha.fields import CaptchaField


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "captcha"]
        widgets = {
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "avatar"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"multiple": False}),
        }
