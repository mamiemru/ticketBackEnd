# Generated by Django 4.1.5 on 2023-05-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0036_unvalidatedticketdecaisse_remove_userapikey_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachementimageticket',
            name='type',
            field=models.CharField(choices=[('ticket', 'Ticket'), ('recepiece', 'Receipiece'), ('facture', 'Facture'), ('unnammed', 'None')], max_length=10, null=True),
        ),
    ]
