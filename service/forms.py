from django import forms
from django.conf import settings

from service.validators import max_file_size


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[max_file_size])
