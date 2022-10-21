import io
import zipfile

from django.conf import settings

from service.models import UploadedFile, FileChunk


def handle_uploaded_file(file, request):
    name = '.'.join(file.name.split('.')[:-1])

    uploaded_file = UploadedFile.objects.create(
        name=file.name,
        author=request.user,
        dir_path=f'{name}/',
        size=file.size
    )

    archive_name = settings.MEDIA_ROOT / f'{name}.zip'
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

    with open(archive_name, 'wb+') as f:
        f.write(zip_buffer.getvalue())
