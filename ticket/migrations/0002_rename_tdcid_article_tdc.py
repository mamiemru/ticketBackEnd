# Generated by Django 4.1.5 on 2023-01-23 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='tdcId',
            new_name='tdc',
        ),
    ]
