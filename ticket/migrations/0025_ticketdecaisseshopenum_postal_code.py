# Generated by Django 4.1.5 on 2023-03-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0024_attachementimageticket_api_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdecaisseshopenum',
            name='postal_code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
