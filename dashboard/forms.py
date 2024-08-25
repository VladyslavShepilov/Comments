from django import forms
from captcha.fields import CaptchaField
from .models import Comment


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ["text", "parent", "image", "captcha"]

    def save(self, commit=True, user=None):
        comment = super().save(commit=False)
        if user:
            comment.user = user
        if commit:
            comment.save()
        return comment
