# Generated by Django 4.1.5 on 2023-05-22 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0032_shopenseigne_alter_itemarticletogs1_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketdecaisseshopenum',
            options={'ordering': ['enseigne', 'name']},
        ),
        migrations.AddField(
            model_name='itemarticletogs1',
            name='enseigne',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticket.shopenseigne'),
        ),
    ]