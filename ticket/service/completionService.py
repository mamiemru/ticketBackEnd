

from django.db.models import Q
from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.models import Article
from ticket.models import TicketDeCaisseShopEnum
from ticket.models import AttachementImageArticle
from ticket.serializers import ArticleSerializer
from ticket.serializers import TicketDeCaisseShopEnumSerializer

class CompletionService:
    
    @staticmethod
    def get_changed_shop(api_key: APIKey, shop_id: int):
        """ Using only one shop_id, we retrieve all usefull fields that can be usefull to full out a new TDC
            data_keys object is the dict containning all fields we want to extract.

        Args:
            api_key (_type_): APIKey
            shop_id (int): shop_id

        Returns:
            Dict, 200: if process complet
            None, 404: otherwise
        """
        
        shop_object = TicketDeCaisseShopEnum.objects.get(id=shop_id)
        
        if not shop_object:
            return None, status.HTTP_404_NOT_FOUND
        
        articlesQuery = Article.objects.filter(api_key=api_key, tdc__shop=shop_object)
        
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
        
        datas['tdc'] = TicketDeCaisseShopEnumSerializer(shop_object).data
        datas['quant'] = 1
        datas['remise'] = 0.0
        
        return datas, status.HTTP_200_OK
    
    @staticmethod
    def get_changed_item_article(api_key: APIKey, shop_name: str, item_article_ident: str):
        """ Retrive the Article with item_article_ident and _tdc_shop_name that match with params

        Args:
            api_key (APIKey): APIKey
            shop_name (str): shop_name
            item_article_ident (str): item_article_ident

        Returns:
            Article, 200: if process complet
            None, 404: otherwise
        """
        
        shop_object = TicketDeCaisseShopEnum.objects.filter(name=shop_name).first()
        
        if not shop_object:
            return None, status.HTTP_404_NOT_FOUND
        
        article = Article.objects.filter(Q(tdc__shop=shop_object), Q(item__ident=item_article_ident), api_key=api_key).last()
        
        if not article:
            return None, status.HTTP_404_NOT_FOUND
            
        article.item.attachement = AttachementImageArticle.objects.filter(name=item_article_ident).first()
        return ArticleSerializer(article).data, status.HTTP_200_OK