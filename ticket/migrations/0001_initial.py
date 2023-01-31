# Generated by Django 4.1.5 on 2023-01-23 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feuille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField()),
                ('factures', models.TextField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='ItemArticleCategoryEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('required', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ItemArticleGroupEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TicketDeCaisseLocalisationEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TicketDeCaisseShopEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TicketDeCaisseTypeEnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('required', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TicketDeCaisse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(unique=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticket.ticketdecaissetypeenum')),
                ('localisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticket.ticketdecaisselocalisationenum')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticket.ticketdecaisseshopenum')),
            ],
        ),
        migrations.CreateModel(
            name='ItemArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ident', models.TextField()),
                ('prix', models.TextField()),
                ('name', models.TextField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticket.itemarticlecategoryenum')),
                ('group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticket.itemarticlegroupenum')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remise', models.FloatField(default=0.0)),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.itemarticle')),
                ('tdcId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticketdecaisse')),
            ],
        ),
    ]