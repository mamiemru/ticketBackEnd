# Generated by Django 4.1.5 on 2023-03-06 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0014_delete_duplicate_on_item_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdecaisseshopenum',
            name='city',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticketdecaisseshopenum',
            name='ident',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticketdecaisseshopenum',
            name='localisation',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticketdecaisseshopenum',
            name='name',
            field=models.TextField(null=True),
        ),
    ]
