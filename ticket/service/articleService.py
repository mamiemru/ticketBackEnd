
from typing import Dict

from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.models import Article
from ticket.serializers import ArticleSerializer

class ArticleService:
    
    @staticmethod
    def list(api_key: APIKey, article_item: Dict):
        """ Retrieve all Articles wich had the same item_article as the parameter article_item

        Args:
            api_key (APIKey): APIKey
            article_item (Dict): object with 'ident' as key callable with get method

        Returns:
            List[ArticleSerializer], 200: found
            None, 404: otherwise
        """
        
        article_item_ident = article_item.get('ident', None)
        
        if article_item_ident is None:
            return {"error": "missing or bad url param ?ident="}, status.HTTP_400_BAD_REQUEST
        
        articles = Article.objects.filter(api_key=api_key, item__ident=article_item_ident).all()
        
        if not articles:
            return None, status.HTTP_404_NOT_FOUND
        
        return ArticleSerializer(articles, many=True), status.HTTP_200_OK