
from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.models import Article
from ticket.models import ItemArticle
from ticket.models import ItemArticleGroupEnum
from ticket.models import AttachementImageArticle
from ticket.models import ItemArticleCategoryEnum
from ticket.serializers import ItemArticleSerializer

class ItemArticleService:
    
    @staticmethod
    def update(api_key: APIKey, item_article, pk) -> ItemArticleSerializer:
        required = item_article['category'].get('required', False)
        category = ItemArticleCategoryEnum.objects.get_or_create(name=item_article['category']['name'], required=required)[0]
        group =  ItemArticleGroupEnum.objects.get_or_create(name=item_article['group']['name'])[0] if item_article['group'] else None
        attachement = AttachementImageArticle.objects.filter(id=item_article['attachement']['id']).first() if item_article['attachement'] else None
        
        item = ItemArticle.objects.get(id=item_article['id'])
        item.name = item_article['name']
        item.ident = item_article['ident']
        item.category = category
        item.group = group
        item.attachement = attachement
        item.save()
        
        return ItemArticleSerializer(item), status.HTTP_200_OK
    
    @staticmethod
    def list(api_key: APIKey, item_article):
        
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
        
        return {"results": datas.data}, status.HTTP_200_OK