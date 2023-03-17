
from django.db import transaction

from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.service.dateService import DateService

from ticket.models import Article
from ticket.models import TicketDeCaisse
from ticket.models import ItemArticleGroupEnum
from ticket.models import AttachementImageTicket
from ticket.models import TicketDeCaisseTypeEnum
from ticket.models import TicketDeCaisseShopEnum
from ticket.models import ItemArticleCategoryEnum
from ticket.models import AttachementImageArticle

from ticket.serializers import TicketDeCaisseSerializer

class TicketDeCaisseService:
    
    @staticmethod
    def create(api_key: APIKey, tdc):
        
        tdcId = None
        try:
            with transaction.atomic():
                tdc_date = DateService.dateStrToDateEnglishDateFormat(tdc['date'])
                
                print(f"{tdc_date=}")
                
                tdc_shop : TicketDeCaisseShopEnum = TicketDeCaisseShopEnum(**tdc['shop'])
                if tdc_shop.ident and tdc_shop.id:
                    tdc_shop = TicketDeCaisseShopEnum.objects.filter(
                        id=tdc_shop.id, ident=tdc_shop.ident, name=tdc_shop.name, city=tdc_shop.city, localisation=tdc_shop.localisation
                    ).first()
                else:
                    tdc_shop.ident = tdc_shop.name
                    tdc_shop.save()
                print(f"{tdc_shop=}")
                
                tdc_category = TicketDeCaisseTypeEnum.objects.get_or_create(**tdc['category'])[0]
                print(f"{tdc_category=}")
                
                if not tdc_category or not tdc_shop or not tdc_date:
                    return {'error': 'field empty'}, status.HTTP_400_BAD_REQUEST
                
                if tdc['attachement']:
                    tdc_attachement = AttachementImageTicket.objects.filter(id=tdc['attachement']['id']).first()
                else:
                    tdc_attachement = None
                print(f"{tdc_attachement=}")
                
                tdc = TicketDeCaisse.objects.get_or_create(shop=tdc_shop, category=tdc_category, date=tdc_date, attachement=tdc_attachement)
                if not tdc[1]:
                    raise Exception("Ticket de caisse already exists")
                tdcId = tdc[0].id
                print(tdc, tdcId)
                
                for article in tdc['articles']:
                    if not article['item'] or not article['item']['category']:
                        raise Exception("one field is empty")
                    
                    required = article['item']['category'].get('required', False)
                    category = ItemArticleCategoryEnum.objects.get_or_create(name=article['item']['category']['name'], required=required)[0]
                    print(category)
                    group =  ItemArticleGroupEnum.objects.get_or_create(name=article['item']['group']['name'])[0] if article['item']['group'] else None
                    print(group)
                    attachement = AttachementImageArticle.objects.filter(id=article['item']['attachement']['id']).first() if article['item']['attachement'] else None
                    print(attachement)
                    item = ItemArticle.objects.get_or_create(
                        name=article['item']['name'], ident=article['item']['ident'], category=category, group=group, attachement=attachement
                    )
                    print(item)
                    
                    tdc_article = Article( tdc=tdc[0], remise=article['remise'], quantity=article['quantity'], price=article['price'], item=item[0] )
                    tdc_article.save()
                    print(tdc_article)
        except Exception as e:
            return {'error': str(e)}, status.HTTP_400_BAD_REQUEST
               
        new_tdc = TicketDeCaisse.objects.get(id=tdcId)
        new_tdc.articles = Article.objects.filter(tdc=new_tdc)
        datas = TicketDeCaisseSerializer(new_tdc)
        return datas.data, status.HTTP_201_CREATED