

from django.db.models import Q
from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.models import Article
from ticket.models import TicketDeCaisseShopEnum
from ticket.models import AttachementImageArticle
from ticket.serializers import ArticleSerializer
from ticket.serializers import TicketDeCaisseShopEnumSerializer

from rest_framework import status
from rest_framework_api_key.models import APIKey

class CompletionService:
    
    @staticmethod
    def get(api_key, shop_id: int):
        shopObj = TicketDeCaisseShopEnum.objects.get(id=shop_id)
        
        if not shopObj:
            return None, status.HTTP_404_NOT_FOUND
        
        articlesQuery = Article.objects.filter(api_key=api_key, tdc__shop=shopObj)
        
        data_keys = { 
            'tdc_category': 'tdc__category__name',
            'item_ident': 'item__ident',
            'item_category': 'item__category__name',
            'item_name': 'item__name',
            'item_group': 'item__group__name',
            'item_brand': 'item__brand__name'
        }
        
        datas = {
            k: [l[v] for l in articlesQuery.values(v).distinct().order_by(v)] for k,v in data_keys.items()
        }
        
        datas['tdc'] = TicketDeCaisseShopEnumSerializer(shopObj).data
        datas['quant'] = 1
        datas['remise'] = 0.0
        
        return datas, status.HTTP_200_OK
    
    @staticmethod
    def get2(api_key: APIKey, shop: str, ident: str):
        shopObj   = TicketDeCaisseShopEnum.objects.filter(name=shop).first()
        
        if not shopObj:
            return None, status.HTTP_404_NOT_FOUND
        
        article = Article.objects.filter(Q(tdc__shop=shopObj), Q(item__ident=ident), api_key=api_key).last()
        
        if not article:
            return None, status.HTTP_404_NOT_FOUND
            
        article.item.attachement = AttachementImageArticle.objects.filter(name=ident).first()
        return ArticleSerializer(article).data, status.HTTP_200_OK