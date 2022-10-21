from django.core.exceptions import ValidationError
from django.conf import settings


def max_file_size(value):
    filesize = value.size
    
    if filesize > settings.MAX_FILE_SIZE:
        raise ValidationError("You cannot upload file more than 16Mb")
    return value
