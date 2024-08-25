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
        fields = ["text", "parent", "captcha", "file", "image"]

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        cleaned_text = bleach.clean(
            text,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )
        return cleaned_text

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")
        if uploaded_file:
            try:
                validate_text_file_extension(uploaded_file)
                validate_text_file_size(uploaded_file)
            except ValidationError:
                raise ValidationError(
                    "Invalid text file. Please ensure it is a TXT file and does not exceed the size limit."
                )
        return uploaded_file

    def clean_image(self):
        uploaded_image = self.cleaned_data.get("image")
        if uploaded_image:
            try:
                validate_image_extension(uploaded_image)
                validate_image_size(uploaded_image)
                validate_image_file(uploaded_image)
                img = Image.open(uploaded_image)
                img.verify()
            except (IOError, SyntaxError, ValidationError):
                raise ValidationError(
                    "Invalid image file. Please ensure it is a supported image format and does not exceed the size or dimension limits."
                )
        return uploaded_image

    def save(self, commit=True, user=None):
        comment = super().save(commit=False)
        if user:
            comment.user = user
        if commit:
            comment.save()
        return comment
