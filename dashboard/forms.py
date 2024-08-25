from django import forms
import bleach
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError

from .models import Comment


ALLOWED_TAGS = {"a", "code", "i", "strong"}
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"]
}


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text", "parent", "image"]

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        cleaned_text = bleach.clean(
            text,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )

        try:
            bleach.linkify(cleaned_text)
        except Exception as e:
            raise ValidationError("Unable to convert : {} ".format(e))

        return cleaned_text

    def save(self, commit=True, user=None):
        comment = super().save(commit=False)
        if user:
            comment.user = user
        if commit:
            comment.save()
        return comment
