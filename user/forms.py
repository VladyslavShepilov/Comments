from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from captcha.fields import CaptchaField
from django.contrib.auth.forms import PasswordChangeForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["username", "email", "captcha"]
        widgets = {
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput()
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "avatar"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"multiple": False}),
        }


class OptionalPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].required = False
        self.fields["new_password1"].required = False
        self.fields["new_password2"].required = False

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 or new_password2:
            if not new_password1 or not new_password2:
                self.add_error("new_password2", "Both password fields must be filled if changing password.")
            elif new_password1 != new_password2:
                self.add_error("new_password2", "The two new password fields must match.")

        return cleaned_data

    def save(self, commit=False):
        if self.cleaned_data.get("new_password1") and self.cleaned_data.get("new_password2"):
            return super().save(commit=False)
        return self.user
