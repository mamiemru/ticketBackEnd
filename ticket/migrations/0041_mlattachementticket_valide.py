# Generated by Django 4.1.5 on 2023-06-07 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0040_alter_mlattachementticket_attachement'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlattachementticket',
            name='valide',
            field=models.BooleanField(default=False),
        ),
    ]
