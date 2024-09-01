import os
import uuid
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser


def get_default_avatar():
    return "images/default_profile.png"


def profile_image_file_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/user_images/", filename)


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    avatar = models.ImageField(
        upload_to=profile_image_file_path,
        default=get_default_avatar,
        null=True,
    )
