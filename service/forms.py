from django import forms

from service.validators import max_file_size, unique_file_name


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[max_file_size, unique_file_name])
