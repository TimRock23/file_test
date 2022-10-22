import io
import zipfile

from django.conf import settings

from service.models import UploadedFile, FileChunk


def handle_uploaded_file(file, request):
    uploaded_file = UploadedFile.objects.create(
        name=file.name,
        author=request.user,
        size=file.size
    )

    archive_path = settings.MEDIA_ROOT / uploaded_file.archive_name
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for ind, chunk in enumerate(file.chunks(chunk_size=settings.MAX_CHUNK_SIZE), 1):
            file_name = f'{ind}.bin'
            zip_file.writestr(file_name, chunk)
            FileChunk.objects.create(
                file=uploaded_file,
                index=ind,
                size=len(chunk)
            )

    with open(archive_path, 'wb+') as f:
        f.write(zip_buffer.getvalue())


def get_file_for_download(file):
    zip_buffer = io.BytesIO()
    zip_path = settings.MEDIA_ROOT / file.archive_name
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for f in zip_ref.namelist():
            zip_buffer.write(zip_ref.read(f))
    return zip_buffer
