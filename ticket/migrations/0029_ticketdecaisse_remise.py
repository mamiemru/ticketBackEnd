# Generated by Django 4.1.5 on 2023-04-27 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0028_ticketdecaisseshopenum_valide'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdecaisse',
            name='remise',
            field=models.FloatField(default=0.0),
        ),
    ]