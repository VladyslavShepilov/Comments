import os
import uuid
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model

from .validators import (
    validate_image_extension,
    validate_image_size,
    validate_image_file,
    validate_text_file_size,
    validate_text_file_extension,
)


def image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.id)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/comment_images/", filename)


def file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.created_at)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/comment_files/", filename)


class Comment(models.Model):
    text = models.TextField()
    image = models.ImageField(
        upload_to=image_file_path,
        null=True,
        blank=True,
        validators=[validate_image_extension, validate_image_size, validate_image_file],
    )
    file = models.FileField(
        upload_to=file_path,
        null=True,
        blank=True,
        validators=[validate_text_file_size, validate_text_file_extension],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), related_name="comments", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"{self.user.username} at ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"
        )

    class Meta:
        ordering = ["-created_at"]
