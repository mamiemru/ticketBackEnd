# Generated by Django and I, 4.1.5 on 2023-02-05 08:45

from django.db.models import F
from django.db import migrations, models

def copy_price_field(apps, schema):
    itemarticles = apps.get_model('ticket', 'ItemArticle')
    articles = apps.get_model('ticket', 'article')
    for ia in itemarticles.objects.all():
        articles.objects.filter(item=ia).update(price=ia.prix)
    
class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0010_attachementimageticket_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='price',
            field=models.FloatField(default=-1)
        ),
        migrations.RunPython(code=copy_price_field),
        migrations.RemoveField(
            model_name='ItemArticle',
            name='prix',
        )
    ]
