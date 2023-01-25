
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
        
class TicketDeCaisseShopEnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDeCaisseShopEnum
        fields = '__all__'
        
class TicketDeCaisseLocalisationEnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDeCaisseLocalisationEnum
        fields = '__all__'
            
class ItemArticleGroupEnumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemArticleGroupEnum
        fields = '__all__'
            
class ItemArticleSerializer(serializers.ModelSerializer):
    category = ItemArticleCategoryEnumSerializer(read_only=True)
    group = ItemArticleGroupEnumSerializer(read_only=True)
    class Meta:
        model = ItemArticle
        fields = '__all__'
                
class ArticleSerializer(serializers.ModelSerializer):
    item = ItemArticleSerializer(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        
class TicketDeCaisseSerializer(serializers.ModelSerializer):
    
    shop = TicketDeCaisseShopEnumSerializer(read_only=True)
    localisation = TicketDeCaisseLocalisationEnumSerializer(read_only=True)
    category = TicketDeCaisseTypeEnumSerializer(read_only=True)
    articles = ArticleSerializer(read_only=True, many=True)
    total = serializers.ReadOnlyField()
    
    class Meta:
        model = TicketDeCaisse
        fields = ('id', 'shop', 'localisation', 'date', 'category', 'articles', 'total')
                                
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
        
class DatabaseRowSerializer(serializers.Serializer):
    shop = serializers.ListField(required=False)
    localisation = serializers.ListField(required=False)
    category = serializers.ListField(required=False)
    item_article_category = serializers.ListField(required=False)
    item_article = serializers.ListField(required=False)
    item_article_ident = serializers.ListField(required=False)
    price = serializers.ListField(required=False)
    group = serializers.ListField(required=False)
    articleQuant = serializers.ReadOnlyField(required=False)
    articleRemise = serializers.ReadOnlyField(required=False)
    
    class Meta:
        fields = '__all__'
        
class AttachementsImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AttachementsImages
        fields = '__all__'