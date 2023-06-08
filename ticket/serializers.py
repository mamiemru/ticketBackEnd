
import json

from rest_framework import serializers

from .models import *

class TicketDeCaisseTypeEnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDeCaisseTypeEnum
        fields = '__all__'

class ItemArticleCategoryEnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemArticleCategoryEnum
        fields = '__all__'
        
class ItemArticleBrandEnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemArticleBrandEnum
        fields = '__all__'
        
class ShopEnseigneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopEnseigne
        fields = '__all__'
        
class TicketDeCaisseShopEnumSerializer(serializers.ModelSerializer):
    enseigne = ShopEnseigneSerializer()
    class Meta:
        model = TicketDeCaisseShopEnum
        fields = '__all__'
            
class ItemArticleGroupEnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemArticleGroupEnum
        fields = '__all__'
        
class AttachementImageTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachementImageTicket
        fields = ('id', 'name', 'category', 'type', 'image')
        
class AttachementImageArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachementImageArticle
        fields = '__all__'
         
class ItemArticleSerializer(serializers.ModelSerializer):
    category = ItemArticleCategoryEnumSerializer()
    group = ItemArticleGroupEnumSerializer()
    brand = ItemArticleBrandEnumSerializer()
    attachement = AttachementImageArticleSerializer(read_only=True)
    class Meta:
        model = ItemArticle
        fields = '__all__'
        
class TicketDeCaisseHeaderSerializer(serializers.ModelSerializer):
    shop = TicketDeCaisseShopEnumSerializer()
    category = TicketDeCaisseTypeEnumSerializer()
    
    class Meta:
        model = TicketDeCaisse
        fields = ('id', 'shop', 'date', 'category', 'total', 'type', 'need_to_be_validated')
               
class ArticleSerializer(serializers.ModelSerializer):
    item = ItemArticleSerializer()
    tdc = TicketDeCaisseHeaderSerializer()
    class Meta:
        model = Article
        fields = ('item', 'tdc', 'price', 'remise', 'quantity')

class TicketDeCaisseSerializer(serializers.ModelSerializer):
    
    shop = TicketDeCaisseShopEnumSerializer()
    category = TicketDeCaisseTypeEnumSerializer()
    articles = ArticleSerializer(many=True, required=False)
    attachement = AttachementImageTicketSerializer()
    
    class Meta:
        model = TicketDeCaisse
        exclude = ('api_key', )

class FeuilleSerializer(serializers.ModelSerializer):
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    factures_json = serializers.ReadOnlyField()
    tickets = serializers.ReadOnlyField()
    
    class Meta:
        model = Feuille
        fields = ('id', 'date', 'year', 'month', 'factures_json', 'tickets')

class FeuilleSummarySerializer(serializers.Serializer):
    tttheorique_v = serializers.ReadOnlyField()
    ttdepense = serializers.ReadOnlyField()
    factures = serializers.ReadOnlyField()
    ttevitable = serializers.ReadOnlyField()
    tteparge = serializers.ReadOnlyField()
    ttconfort = serializers.ReadOnlyField()
    dep = serializers.ReadOnlyField()
    mj = serializers.ReadOnlyField()
    
    class Meta:
        fields = '__all__'
        
class AttachementsImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AttachementsImages
        fields = '__all__'           
         
class AttachementImageArticleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AttachementImageArticle
        fields = '__all__'
        
class CompletionChangedSerilizer(serializers.Serializer):
    shops: serializers.SerializerMethodField()
    categories: serializers.SerializerMethodField()
    
    class Meta:
        fields = '__all__'


class MlAttachementTicketSerializer(serializers.ModelSerializer):
    attachement = AttachementImageTicketSerializer(read_only=True)
    tdc = serializers.SerializerMethodField(read_only=True)
    gcp_datas = serializers.ReadOnlyField()
    
    class Meta:
        model = MLAttachementTicket
        fields = '__all__'
        
    def get_tdc(self, obj):
        tdc : TicketDeCaisse = TicketDeCaisse.objects.filter(attachement=obj.attachement).last()
        if not tdc:
            return None
        return TicketDeCaisseHeaderSerializer(tdc).data


class MlAttachementTicketHeaderSerializer(serializers.ModelSerializer):
    attachement = AttachementImageTicketSerializer(read_only=True)
    tdc = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = MLAttachementTicket
        fields = ('id', 'attachement', 'valide', 'tdc')
        
    def get_tdc(self, obj):
        tdc : TicketDeCaisse = TicketDeCaisse.objects.filter(attachement=obj.attachement).last()
        if not tdc:
            return None
        return TicketDeCaisseHeaderSerializer(tdc).data
