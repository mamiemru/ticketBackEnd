# Generated by Django 4.1.5 on 2023-03-13 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0017_remove_ticketdecaisse_localisation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datas', models.TextField(default='{}')),
            ],
        ),
    ]
