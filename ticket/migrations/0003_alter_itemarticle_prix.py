# Generated by Django 4.1.5 on 2023-01-23 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_rename_tdcid_article_tdc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemarticle',
            name='prix',
            field=models.FloatField(),
        ),
    ]
