# Generated by Django 4.1.5 on 2023-01-25 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_alter_itemarticle_prix'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachementsImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('category', models.CharField(choices=[('ticket', 'Ticket'), ('article', 'Article'), ('icon', 'Icon')], max_length=10)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.AlterModelOptions(
            name='feuille',
            options={'ordering': ['-date']},
        ),
    ]