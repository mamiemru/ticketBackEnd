
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
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.models import AbstractAPIKey

from ticket.storage.jpegStorage import JpegStorage
from ticket.storage.jpegStorage import iso_date_prefix

class TicketDeCaisseTypeEnum(Model):
    name = TextField(null=False)
    required = BooleanField(null=False, default=False)
    description = TextField(null=True, default="", max_length=255)
    
    def __str__(self):
        return f"TicketDeCaisseTypeEnum(name={self.name}, required={self.required})"
        
class ItemArticleCategoryEnum(Model):
    name = TextField(null=False)
    required = BooleanField(null=False, default=False)
    
    def __str__(self):
        return f"ItemArticleCategoryEnum(name={self.name}, required={self.required})"

class TicketDeCaisseShopEnum(Model):
    ident = TextField(null=False)
    name = TextField(null=True)
    city = TextField(null=False)
    localisation = TextField(null=False)
    
    def __str__(self):
        return f"TicketDeCaisseShopEnum({self.ident=}, {self.name=}, {self.city=}, {self.localisation=})"
    
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
    image = ImageField(upload_to='articles', null=False, storage=JpegStorage(bucket_name='article'))
    def __str__(self):
        return f"AttachementImageArticle(category={self.category}, name={self.name}, img={self.image})"

class AttachementImageTicket(Model):
    name = TextField(max_length=50, null=False)
    category = CharField(default='ticket', null=False, editable=False, max_length=6)
    type = CharField(null=False, choices = (('ticket', 'Ticket'), ('recepiece', 'Receipiece'), ('facture', 'Facture')), max_length=10)
    image = ImageField(upload_to=iso_date_prefix, null=False, storage=JpegStorage(bucket_name='ticket'))
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
    date = DateTimeField(null=False)
    category = ForeignKey(TicketDeCaisseTypeEnum, to_field='id', null=True, on_delete=SET_NULL)
    attachement = ForeignKey(AttachementImageTicket, to_field='id', null=True, on_delete=SET_NULL)
    api_key = ForeignKey(APIKey, on_delete=SET_NULL, null=True)
    
    def __str__(self):
        return f"TicketDeCaisse(api_key={self.api_key}, shop={self.shop}, date={self.date}, category={self.category}, attachement={self.attachement})"
    
    def total(self):
        return round(math.fsum([article.price for article in Article.objects.filter(tdc=self.id)]), 2)
    
    def sum_total(self, articles : List):
        return round(math.fsum([article.price for article in articles]), 2)
    
class Article(Model):
    item = ForeignKey(ItemArticle, to_field='id', on_delete=CASCADE)
    price = FloatField(null=False)
    remise = FloatField(null=False, default=0.0)
    quantity = IntegerField(null=False, default=1)
    tdc = ForeignKey(TicketDeCaisse, on_delete=CASCADE)
    api_key = ForeignKey(APIKey, on_delete=SET_NULL, null=True)
    
    def __str__(self):
        return f"Article(api_key={self.api_key}, {self.remise=}, quantity={self.quantity}, price={self.price}, tdc={self.tdc}, item={self.item})"
    
class Feuille(Model):
    date = IntegerField(null=False)
    factures = TextField(null=False, default="{}")
    api_key = ForeignKey(APIKey, on_delete=SET_NULL, null=True)
    
    class Meta:
        ordering  = ['-date']
    
    def __str__(self):
        return f"Feuille(api_key={self.api_key}, date={self.date}, factures={self.factures})"

    def year(self):
        return datetime.datetime.fromtimestamp(self.date).year
        
    def month(self):
        return datetime.datetime.fromtimestamp(self.date).month
    
    def factures_json(self):
        return json.loads(self.factures)

class Factures(Model):
    datas = TextField(null=False, default="{}")
    api_key = ForeignKey(APIKey, on_delete=SET_NULL, null=True)
    
    def __str__(self):
        return f"Factures(api_key={self.api_key}, {self.datas=})"
    
## ====================================================================================================
##
##  API KEYS MODELS
##
## ====================================================================================================

class Profile(Model):
    name = CharField(max_length=128)

class UserApiKey(AbstractAPIKey):
    profile = ForeignKey(Profile, on_delete=SET_NULL, null=True, related_name="api_keys")
