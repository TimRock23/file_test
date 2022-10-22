from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from service.forms import UploadFileForm
from service.models import UploadedFile
from service.utils import handle_uploaded_file, get_file_for_download


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
def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    if request.user != file.author:
        return redirect('service:index')

    prepared_file = get_file_for_download(file)
    response = HttpResponse(prepared_file.getvalue(), content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response


@login_required
def user_files(request):
    files = request.user.files.all()
    return render(request, 'service/download.html', {'files': files})
