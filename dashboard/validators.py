from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError


# Image validators
def validate_image_extension(image):
    valid_extensions = ["jpg", "jpeg", "png", "gif"]
    ext = image.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension. Please upload JPG, GIF, or PNG files.")


def validate_image_size(image):
    width, height = get_image_dimensions(image)
    if width > 320 or height > 240:
        raise ValidationError("Image dimensions must be no larger than 320x240 pixels.")


def validate_image_file(image):
    file_size = image.file.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb}MB.")


# Text validators
def validate_text_file_size(file):
    max_size_mb = 0.1
    file_size = file.file.size
    if file_size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size should not exceed {max_size_mb * 1024} KB.")


def validate_text_file_extension(file):
    valid_extensions = ["txt"]
    ext = file.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension. Please upload TXT files only.")
