from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model 

User = get_user_model()


class UploadedFile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='files')
    size = models.PositiveIntegerField(
        validators=[MaxValueValidator(settings.MAX_FILE_SIZE)]
    )

    @property
    def archive_name(self):
        name = '.'.join(self.name.split('.')[:-1])
        return f'{name}.zip'


class FileChunk(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE,
                             related_name='chunks')
    index = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(settings.MAX_FILE_CHUNKS_COUNT)]
    )
    size = models.PositiveIntegerField(
        validators=[MaxValueValidator(settings.MAX_CHUNK_SIZE)]
    )

    class Meta:
        ordering = ['-index']
        constraints = [
            models.UniqueConstraint(
                fields=['file', 'index'],
                name='file_chunk_index_unique'
            )
        ]
