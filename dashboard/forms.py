from django import forms
import bleach
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from .models import Comment
from .validators import (
    validate_image_extension,
    validate_image_size,
    validate_image_file,
    validate_text_file_size,
    validate_text_file_extension,
)
from PIL import Image

ALLOWED_TAGS = {"a", "code", "i", "strong"}
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"]
}


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ["text", "parent", "captcha", "file"]

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        cleaned_text = bleach.clean(
            text,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )
        return cleaned_text

    def save(self, commit=True, user=None):
        comment = super().save(commit=False)
        uploaded_file = self.cleaned_data.get("file")
        if uploaded_file:
            try:
                img = Image.open(uploaded_file)
                img.verify()
                validate_image_extension(uploaded_file)
                validate_image_size(uploaded_file)
                validate_image_file(uploaded_file)
                comment.image = uploaded_file
                comment.file = None
            except (IOError, SyntaxError, ValidationError):
                validate_text_file_extension(uploaded_file)
                validate_text_file_size(uploaded_file)
                comment.file = uploaded_file
                comment.image = None

        if user:
            comment.user = user
        if commit:
            comment.save()
        return comment
