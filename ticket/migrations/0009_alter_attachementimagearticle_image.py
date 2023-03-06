# Generated by Django 4.1.5 on 2023-01-29 19:05

from django.db import migrations, models
import django_minio_backend.models

from ticket.storage.jpegStorage import JpegStorage

class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0008_itemarticle_attachement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachementimagearticle',
            name='image',
            field=models.ImageField(storage=JpegStorage(bucket_name='article'), upload_to='articles'),
        ),
    ]
