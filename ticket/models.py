
import json
import math
import datetime

from typing import List

from django.db.models import Model
from django.db.models import TextChoices
from django.db.models import CASCADE
from django.db.models import SET_NULL
from django.db.models import JSONField
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import FloatField
from django.db.models import ImageField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import BooleanField
from django.db.models import DateTimeField
from django.db.models import OneToOneField
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.models import AbstractAPIKey

from ticket.storage.jpegStorage import JpegStorage
from ticket.storage.jpegStorage import iso_date_prefix

def image_path(instance, filename):
    return f'images/{instance.category}/{filename}'

class TicketDeCaisseTypeEnum(Model):
    name = TextField(null=False)
    required = BooleanField(null=False, default=False)
    description = TextField(null=True, default="", max_length=255)
    
    def __str__(self):
        return f"TicketDeCaisseTypeEnum(name={self.name}, required={self.required})"
    
    def get_or_create_tdc_type_by_args(kwargs):
        print(f"TicketDeCaisseTypeEnum.get_or_create_tdc_type_by_args({kwargs=})")
        return TicketDeCaisseTypeEnum.objects.get_or_create(**kwargs)[0]
        
class ItemArticleCategoryEnum(Model):
    name = TextField(null=False)
    required = BooleanField(null=False, default=False)
    
    def __str__(self):
        return f"ItemArticleCategoryEnum(name={self.name}, required={self.required})"

    class Meta:
        ordering = ["name", "required"]
        
    def get_ia_category_by_name_or_none(name):
        return ItemArticleCategoryEnum.objects.filter(name=name).last() if name else None
        
class ShopEnseigne(Model):
    name = TextField(null=False)
    icon = ImageField(upload_to='enseignes', null=False, storage=JpegStorage(bucket_name='enseignes'))
    
    def __str__(self):
        return f"ShopEnseigne({self.id=}, {self.name=})"

class TicketDeCaisseShopEnum(Model):
    enseigne = ForeignKey(ShopEnseigne, null=True, default=None, on_delete=SET_NULL)
    ident = TextField(null=False)
    name = TextField(null=True)
    city = TextField(null=False)
    postal_code = IntegerField(null=False)
    localisation = TextField(null=False)
    valide = BooleanField(default=True, null=False)
    
    def __str__(self):
        return f"TicketDeCaisseShopEnum({self.enseigne} {self.ident}, {self.name}, {self.city=}, {self.postal_code=}, {self.localisation=}, {self.valide=})"
    
    class Meta:
        ordering = ["enseigne", "name"]
        
    @staticmethod
    def not_confirmed_tdcshop_object(shop_ident: str):
        return TicketDeCaisseShopEnum(
            ident=shop_ident, name=shop_ident, valide=False
        )
        
    @staticmethod
    def empty_tdcshop_object():
        return TicketDeCaisseShopEnum(ident=None, valide=False)
    
class ItemArticleGroupEnum(Model):
    name = TextField(null=False)
    
    def __str__(self):
        return f"ItemArticleGroupEnum(name={self.name})"
    
    class Meta:
        ordering = ["name"]
        
    @staticmethod
    def get_group_by_name_or_none(group_object):
        return ItemArticleGroupEnum.objects.get_or_create(name=group_object['name'])[0] if group_object else None

class ItemArticleBrandEnum(Model):
    name = TextField(null=False)
    
    def __str__(self):
        return f"ItemArticleBrandEnum(name={self.name})"

    class Meta:
        ordering = ["name"]
        
    def get_brand_by_name_or_none(brand_object):
        return ItemArticleBrandEnum.objects.get_or_create(name=brand_object['name'])[0] if brand_object else None

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
    
    class Meta:
        ordering = ["name"]
        
    @staticmethod
    def get_attachement_by_id_or_none(attachement):
        return AttachementImageArticle.objects.filter(id=attachement['id']).first() if attachement else None

class AttachementImageTicket(Model):
    name = TextField(max_length=50, null=False)
    category = CharField(default='ticket', null=False, editable=False, max_length=6)
    type = CharField(null=True, choices = (('ticket', 'Ticket'), ('recepiece', 'Receipiece'), ('facture', 'Facture'), ('unnammed', 'None')), max_length=10)
    image = ImageField(upload_to=iso_date_prefix, null=False, storage=JpegStorage(bucket_name='ticket'))
    api_key = ForeignKey(APIKey, on_delete=SET_NULL, null=True)
    
    def __str__(self):
        return f"AttachementImageTicket(api_key={self.api_key}, category={self.category}, type={self.type}, name={self.name}, img={self.image})"
    
class ItemArticle(Model):
    
    class JunkScoreChoices(TextChoices):
        NOT_ASSIGNED = 0, ("No Value")
        GREEN = 1, ("OK")
        ORANGE = 2, ("COULD BE AVOIDED")
        RED = 3, ("SHOULD BE AVOIDED")
        BLACK = 4, ("MUST BE AVOIDED")
    
    ean13 = TextField(null=True)
    ident = TextField(null=False)
    name = TextField(null=False)
    junkscore = CharField(null=True, max_length=1, choices=JunkScoreChoices.choices, default=JunkScoreChoices.NOT_ASSIGNED)
    brand = ForeignKey(ItemArticleBrandEnum, to_field='id', null=True, default=None, on_delete=SET_NULL)
    category = ForeignKey(ItemArticleCategoryEnum, to_field='id', null=True, default=None, on_delete=SET_NULL)
    group = ForeignKey(ItemArticleGroupEnum, to_field='id', null=True, default=None, on_delete=SET_NULL)
    attachement = ForeignKey(AttachementImageArticle, to_field='id', default=None, null=True, on_delete=SET_NULL)
    
    def __str__(self):
        return f"ItemArticle(id={self.id} #{self.ean13} ident={self.ident}, brand={self.brand}, name={self.name}, category={self.category}, group={self.group})"
    
    class Meta:
        ordering = ["ident"]
        
class TicketDeCaisse(Model):
    shop = ForeignKey(TicketDeCaisseShopEnum, on_delete=SET_NULL, null=True)
    date = DateTimeField(null=False)
    category = ForeignKey(TicketDeCaisseTypeEnum, to_field='id', null=True, on_delete=SET_NULL)
    attachement = ForeignKey(AttachementImageTicket, to_field='id', null=True, on_delete=SET_NULL)
    api_key = ForeignKey(APIKey, on_delete=SET_NULL, null=True)
    total = FloatField(null=False, default=0.0)
    type = CharField(null=False, choices=(('ticket', 'Ticket'), ('recepiece', 'Receipiece'), ('facture', 'Facture')), max_length=10)
    remise = FloatField(null=False, default=0.0)
    need_to_be_validated = BooleanField(null=False, default=False)
    
    def __str__(self):
        return f"TicketDeCaisse({self.__dict__})"
    
    @staticmethod
    def sum_total(articles : List):
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
    

class ItemArticleToGS1(Model):
    shop = ForeignKey(TicketDeCaisseShopEnum, on_delete=SET_NULL, null=True)
    enseigne = ForeignKey(ShopEnseigne, on_delete=SET_NULL, null=True)
    ean13 = TextField(null=False, unique=False, default=None)
    ident = TextField(null=False, unique=True)
    
    def __str__(self):
        return f"ItemArticleToGS1(id={self.id} #{self.ean13} ident={self.ident}, {self.enseigne})"
    
    class Meta:
        ordering = ["id"]


class MLAttachementTicket(Model):
    attachement = OneToOneField(AttachementImageTicket, on_delete=CASCADE, null=False)
    json_datas = JSONField(null=False)
    gcp_datas = JSONField(null=False)
    valide = BooleanField(null=False, default=False)
    
    def __str__(self):
        return f"MLAttachementTicket(id={self.id}, valide={self.valide}, attachement={self.attachement}, json_datas={len(self.json_datas) > 2}, gcp_datas={len(self.gcp_datas) > 2})"
    
    class Meta:
        ordering = ['id', 'valide', 'attachement']
