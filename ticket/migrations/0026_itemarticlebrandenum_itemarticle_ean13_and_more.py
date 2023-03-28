# Generated by Django 4.1.5 on 2023-03-27 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0025_ticketdecaisseshopenum_postal_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemArticleBrandEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='itemarticle',
            name='ean13',
            field=models.TextField(default=0, unique=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemarticle',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticket.itemarticlebrandenum'),
        ),
    ]