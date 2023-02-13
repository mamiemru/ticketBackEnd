
import json
import math
import datetime

from typing import List

from django.db.models import Model
from django.db.models import CASCADE
from django.db.models import SET_NULL
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import AutoField
from django.db.models import FloatField
from django.db.models import ImageField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import BooleanField
from django.db.models import DateTimeField
from django.db.models import UniqueConstraint

from django_minio_backend import MinioBackend, iso_date_prefix

class TicketDeCaisseTypeEnum(Model):
    name = TextField(null=False)
    required = BooleanField(null=False, default=False)
    
    def __str__(self):
        return f"TicketDeCaisseTypeEnum(name={self.name}, required={self.required})"
        
class ItemArticleCategoryEnum(Model):
    name = TextField(null=False)
    required = BooleanField(null=False, default=False)
    
    def __str__(self):
        return f"ItemArticleCategoryEnum(name={self.name}, required={self.required})"

class TicketDeCaisseShopEnum(Model):
    name = TextField(null=False)
    
    def __str__(self):
        return f"TicketDeCaisseShopEnum(name={self.name})"
    
class TicketDeCaisseLocalisationEnum(Model):
    name = TextField(null=False)
    
    def __str__(self):
        return f"TicketDeCaisseLocalisationEnum(name={self.name})"
    
class ItemArticleGroupEnum(Model):
    name = TextField(null=False)
    
    def __str__(self):
        return f"ItemArticleGroupEnum(name={self.name})"
    
def image_path(instance, filename):
    return f'images/{instance.category}/{filename}'
    
class AttachementsImages(Model): 
    name = TextField(max_length=50, null=False)
    category = CharField(null=False, choices = (('ticket', 'Ticket'), ('article', 'Article'), ('icon', 'Icon')), max_length=10)
    image = ImageField(upload_to=image_path, null=False)
    
    def __str__(self):
        return f"AttachementsImages(category={self.category}, name={self.name}, img={self.image})"

class AttachementImageArticle(Model):
    name = TextField(max_length=50, null=False)
    category = CharField(default='article', null=False, editable=False, max_length=7)
    image = ImageField(upload_to='articles', null=False, storage=MinioBackend(bucket_name='article'))
    def __str__(self):
        return f"AttachementImageArticle(category={self.category}, name={self.name}, img={self.image})"

class AttachementImageTicket(Model):
    name = TextField(max_length=50, null=False)
    category = CharField(default='ticket', null=False, editable=False, max_length=6)
    type = CharField(null=False, choices = (('ticket', 'Ticket'), ('recepiece', 'Receipiece'), ('facture', 'Facture')), max_length=10)
    image = ImageField(upload_to=iso_date_prefix, null=False, storage=MinioBackend(bucket_name='ticket'))
    def __str__(self):
        return f"AttachementImageTicket(category={self.category}, type={self.name}, name={self.name}, img={self.image})"
    
class ItemArticle(Model):
    ident = TextField(null=False)
    name = TextField(null=False)
    category = ForeignKey(ItemArticleCategoryEnum, to_field='id', null=True, on_delete=SET_NULL)
    group = ForeignKey(ItemArticleGroupEnum, to_field='id', null=True, default=None, on_delete=SET_NULL)
    attachement = ForeignKey(AttachementImageArticle, to_field='id', null=True, on_delete=SET_NULL)
    
    def __str__(self):
        return f"ItemArticle(id={self.id}, ident={self.ident}, name={self.name}, category={self.category}, group={self.group})"
        
class TicketDeCaisse(Model):
    shop = ForeignKey(TicketDeCaisseShopEnum, on_delete=SET_NULL, null=True)
    localisation = ForeignKey(TicketDeCaisseLocalisationEnum, on_delete=SET_NULL, null=True)
    date = DateTimeField(null=False, unique=True)
    category = ForeignKey(TicketDeCaisseTypeEnum, to_field='id', null=True, on_delete=SET_NULL)
    attachement = ForeignKey(AttachementImageTicket, to_field='id', null=True, on_delete=SET_NULL)
    
    def __str__(self):
        return f"TicketDeCaisse(shop={self.shop}, localisation={self.localisation}, date={self.date}, category={self.category}, attachement={self.attachement})"
    
    def total(self):
        return math.fsum([article.price for article in Article.objects.filter(tdc=self.id)])
    
    def sum_total(self, articles : List):
        return math.fsum([article.price for article in articles])
    
class Article(Model):
    item = ForeignKey(ItemArticle, to_field='id', on_delete=CASCADE)
    price = FloatField(null=False)
    remise = FloatField(null=False, default=0.0)
    quantity = IntegerField(null=False, default=1)
    tdc = ForeignKey(TicketDeCaisse, on_delete=CASCADE)
    
    def __str__(self):
        return f"Article(remise={self.remise}, quantity={self.quantity}, price={self.price}, tdc={self.tdc}, item={self.item})"
    
class Feuille(Model):
    date = IntegerField(null=False)
    factures = TextField(null=False, default="{}")
    
    class Meta:
        ordering  = ['-date']
    
    def __str__(self):
        return f"Feuille(date={self.date}, factures={self.factures})"

    def year(self):
        return datetime.datetime.fromtimestamp(self.date).year
        
    def month(self):
        return datetime.datetime.fromtimestamp(self.date).month
    
    def factures_json(self):
        return json.loads(self.factures)
