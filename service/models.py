from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model 

User = get_user_model()


class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dir_path = models.FilePathField(allow_files=False, allow_folders=True)
    size = models.PositiveIntegerField(
        validators=[MaxValueValidator(settings.MAX_FIELD_SIZE)]
    )


class FileChunk(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE,
                             related_name='chunks')
    index = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(settings.MAX_FILE_CHUNKS_COUNT)]
    )
    path = models.FilePathField()
    size = models.PositiveIntegerField(
        validators=[MaxValueValidator(settings.MAX_CHUNK_SIZE)]
    )

    class Meta:
        ordering = ['index']
