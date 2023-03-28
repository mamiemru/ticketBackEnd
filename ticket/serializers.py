
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
        
class TicketDeCaisseShopEnumSerializer(serializers.ModelSerializer):
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
        fields = ('name', 'category', 'type', 'image')
        
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
        fields = ('id', 'shop', 'date', 'category', 'total', 'type')
               
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
        fields = ('id', 'shop', 'date', 'category', 'articles', 'total', 'attachement', 'type')

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
        
    def get_shops(self, obj):
        return TicketDeCaisseShopEnumSerializer(TicketDeCaisseShopEnum.objects.all(), many=True)
    
    def get_categories(self, obj):
        return TicketDeCaisseTypeEnumSerializer(TicketDeCaisseTypeEnum.objects.all(), many=True)
    
