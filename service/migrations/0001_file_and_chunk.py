# Generated by Django 4.1.2 on 2022-10-21 05:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dir_path', models.FilePathField(allow_files=False, allow_folders=True)),
                ('size', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(16777216)])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileChunk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(16)])),
                ('path', models.FilePathField()),
                ('size', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1048576)])),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chunks', to='service.uploadedfile')),
            ],
            options={
                'ordering': ['index'],
            },
        ),
    ]
