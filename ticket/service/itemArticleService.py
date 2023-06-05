
from typing import Dict

from rest_framework_api_key.models import APIKey

from ticket.models import Article
from ticket.models import ItemArticle
from ticket.models import ItemArticleGroupEnum
from ticket.models import ItemArticleBrandEnum
from ticket.models import AttachementImageArticle
from ticket.models import ItemArticleCategoryEnum
from ticket.serializers import ItemArticleSerializer

class ItemArticleService:
    
    @staticmethod
    def update(api_key: APIKey, item_article: Dict, pk: str) -> ItemArticleSerializer:
        """ Update ItemArticle object using item_article parameter and pk as ItemArticle.id

        Args:
            api_key (APIKey): APIKey
            item_article (Dict): Dict with ItemArticle fields as key that can be called using brakets
            pk (str): The id of the updated ItemArticle

        Returns:
            ItemArticle, 200: if ok
        """
        
        ean13 = item_article.get('ean13', 0)
        required = item_article['category'].get('required', False)
        category = ItemArticleCategoryEnum.objects.get_or_create(name=item_article['category']['name'], required=required)[0]
        brand =  ItemArticleBrandEnum.get_brand_by_name_or_none(item_article['brand'])
        group =  ItemArticleGroupEnum.get_group_by_name_or_none(item_article['group'])
        attachement = AttachementImageArticle.objects.filter(id=item_article['attachement']['id']).first() if item_article['attachement'] else None
        
        item = ItemArticle.objects.get(id=item_article['id'])
        item.name = item_article['name']
        item.ident = item_article['ident']
        item.brand = brand
        item.category = category
        item.group = group
        item.attachement = attachement
        item.ean13 = ean13
        item.save()
        
        return ItemArticleSerializer(item)
    
    @staticmethod
    def list(api_key: APIKey, item_article: Dict):
        """ List all ItemArticle that match available non null item_article fields

        Args:
            api_key (APIKey): APIKey
            item_article (Dict): Dict of keys that match with Article Object

        Returns:
            Dict: with 'results' keys
        """
        
        ident = item_article.get('item', {}).get('ident', None)
        category = item_article.get('item', {}).get('category', {}).get('name', None)
        group = item_article.get('item', {}).get('group', {}).get('name', None)
        tdcshop = item_article.get('tdc', {}).get('shop', {}).get('name', None)
        tdccategory = item_article.get('tdc', {}).get('category', {}).get('name', None)
        
        articles = Article.objects
        if ident:
            articles = articles.filter(item__ident__icontains=ident.lower())
        if category:
            articles = articles.filter(item__category__name__icontains=category.lower())
        if group:
            articles = articles.filter(item__group__name__icontains=group.lower())
        if tdcshop:
            articles = articles.filter(tdc__shop__name__icontains=tdcshop.lower())
        if tdccategory:
            articles = articles.filter(tdc__category__name__icontains=tdccategory.lower())
            
        itemArticles_ids = articles.values_list('item', flat=True).all()
        itemArticles = ItemArticle.objects.filter(id__in=itemArticles_ids).all()
        datas = ItemArticleSerializer(itemArticles, many=True)
        
        return {"results": datas.data}