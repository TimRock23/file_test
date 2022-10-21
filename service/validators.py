from django.core.exceptions import ValidationError
from django.conf import settings

from service.models import UploadedFile


def max_file_size(value):
    filesize = value.size
    
    if filesize > settings.MAX_FILE_SIZE:
        raise ValidationError("You cannot upload file more than 16Mb")
    return value


def unique_file_name(value):
    filename = value.name
    
    if UploadedFile.objects.filter(name=filename).exists():
        raise ValidationError("We also have file with that name")
    return value
