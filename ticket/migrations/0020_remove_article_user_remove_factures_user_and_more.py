# Generated by Django 4.1.5 on 2023-03-17 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0019_article_user_factures_user_feuille_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='user',
        ),
        migrations.RemoveField(
            model_name='factures',
            name='user',
        ),
        migrations.RemoveField(
            model_name='feuille',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ticketdecaisse',
            name='user',
        ),
    ]