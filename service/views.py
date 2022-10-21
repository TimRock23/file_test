from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

from service.forms import UploadFileForm
from service.utils import handle_uploaded_file


def index(request):
    return render(request, 'service/index.html')


@login_required
def upload_file(request):
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        file = request.FILES['file']
        handle_uploaded_file(file, request)
        return render(request, 'service/success.html', {'file_name': file.name})
    return render(request, 'service/upload.html', {'form': form})


@login_required
def download_file(request):
    pass