from django import forms
from django.conf import settings

from service.validators import max_file_size, unique_name


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[max_file_size, unique_name])
