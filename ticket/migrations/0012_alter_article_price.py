# Generated by Django 4.1.5 on 2023-02-06 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0011_mmigration_price_from_itemarticle_to_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='price',
            field=models.FloatField(),
        ),
    ]
