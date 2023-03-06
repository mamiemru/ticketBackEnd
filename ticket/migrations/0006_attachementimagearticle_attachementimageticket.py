# Generated by Django 4.1.5 on 2023-01-29 12:12

from django.db import migrations, models
import django_minio_backend.models

from ticket.storage.jpegStorage import JpegStorage
from ticket.storage.jpegStorage import iso_date_prefix


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_alter_attachementsimages_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachementImageArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('category', models.CharField(default='article', editable=False, max_length=7)),
                ('image', models.ImageField(storage=JpegStorage(bucket_name='article'), upload_to=iso_date_prefix)),
            ],
        ),
        migrations.CreateModel(
            name='AttachementImageTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('category', models.CharField(default='ticket', editable=False, max_length=6)),
                ('image', models.ImageField(storage=JpegStorage(bucket_name='ticket'), upload_to=iso_date_prefix)),
            ],
        ),
    ]
