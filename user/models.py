import os
import uuid
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/user_images/", filename)


class User(AbstractUser):
    email = models.EmailField(
        unique=True, blank=False, null=False
    )
    avatar = models.ImageField(
        upload_to=profile_image_file_path,
        default="default_profile.png",
        null=True,
    )
