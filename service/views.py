import logging

from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from service.forms import UploadFileForm
from service.models import UploadedFile
from service.utils import handle_uploaded_file, get_file_for_download


logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'service/index.html')


@login_required
def upload_file(request):
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        file = request.FILES['file']

        logger.debug(f'User ID: {request.user.id}. '
                     f'Starting uploading file {file.name}.')
        try:
            handle_uploaded_file(file, request)
        except Exception:
            message = f'Something went wrong with uploading file {file.name}.'
            logger.exception(f'User ID: {request.user.id}. {message}')
            return render(request, 'service/message.html', {'message': message})
        message = f'Successfully uploaded file {file.name}'
        return render(request, 'service/message.html', {'message': message})
    if request.method == 'POST':
        logger.warning(f'User ID: {request.user.id}. '
                       f'Error in File Form validation: {form.errors.as_data()}.')
    return render(request, 'service/upload.html', {'form': form})


@login_required
def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    if request.user != file.author:
        logger.warning(
            f'User ID: {request.user.id}. '
            f'Not author tryed to download file. File made by {file.author.id}'
        )
        return redirect('service:index')

    logger.debug(f'User ID: {request.user.id}. '
                 f'Starting downloading file {file.name}.')
    try:
        prepared_file = get_file_for_download(file)
    except Exception:
        message = f'Something went wrong with downloading file {file.name}.'
        logger.exception(f'User ID: {request.user.id}. {message}')
        return render(request, 'service/message.html', {'message': message})

    response = HttpResponse(prepared_file.getvalue(), content_type='application/force-download')
    if not file.name.isascii():
        logger.info(
            f'User ID: {request.user.id}. Downloading file with non ascii format. '
            f'The name of the downloaded file will be incorrect. File name is: {file.name}.'
        )
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response


@login_required
def user_files(request):
    files = request.user.files.all()
    return render(request, 'service/download.html', {'files': files})
