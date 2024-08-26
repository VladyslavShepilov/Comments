from PIL import Image
from django.core.exceptions import ValidationError


def validate_image_extension(image):
    valid_extensions = ["jpg", "jpeg", "png"]
    extension = image.name.split(".")[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError(
            "Unsupported image extension. Please upload JPG, JPEG, or PNG images."
        )


def validate_image_size(image):
    try:
        img = Image.open(image)
        img.verify()
        img = Image.open(image)
        max_width, max_height = 320, 240
        if img.width > max_width or img.height > max_height:
            raise ValidationError(
                f"Image dimensions must be no larger than {max_width}x{max_height} pixels."
            )
    except (IOError, SyntaxError):
        raise ValidationError("Invalid image file.")


def validate_image_file(image):
    try:
        img = Image.open(image)
        img.verify()
    except (IOError, SyntaxError):
        raise ValidationError("Invalid image file.")


def validate_text_file_size(file):
    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            f"Text file size must be no larger than {max_size_mb} MB."
        )


def validate_text_file_extension(file):
    valid_extensions = ["txt"]
    extension = file.name.split(".")[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError(
            "Unsupported file extension. Please upload TXT files only."
        )
