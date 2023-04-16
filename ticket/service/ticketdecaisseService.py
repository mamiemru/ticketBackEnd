
from django.db import transaction

from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.service.dateService import DateService

from ticket.models import Article
from ticket.models import ItemArticle
from ticket.models import TicketDeCaisse
from ticket.models import ItemArticleBrandEnum
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
        
        new_tdcId = None
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
                
                tdc_type = tdc['type']
                tdc_total = round(tdc['total'], 2)
                
                if not tdc_category or not tdc_shop or not tdc_date or not tdc_type or not tdc_total:
                    return {'error': 'field empty'}, status.HTTP_400_BAD_REQUEST
                
                print(f"{tdc_category=}")
                if tdc['attachement']:
                    if 'id' in tdc['attachement']:
                        tdc_attachement = AttachementImageTicket.objects.filter(id=tdc['attachement']['id']).first()
                    else:
                        tdc_attachement = AttachementImageTicket.objects.filter(**tdc['attachement']).first()
                else:
                    tdc_attachement = None
                
                print(f"{tdc_attachement=}")
                new_tdc = TicketDeCaisse.objects.get_or_create(
                    api_key=api_key, shop=tdc_shop, category=tdc_category, date=tdc_date, attachement=tdc_attachement, type=tdc_type, total=tdc_total
                )
                
                if not new_tdc[1]:
                    raise Exception("Ticket de caisse already exists")
                new_tdcId : int = new_tdc[0].id
                
                print(f"{new_tdc=}")
                for article in tdc['articles']:
                    if not article['item']:
                        raise Exception("one Item field is empty")
                    
                    if tdc_type == 'receipece' and not article['item']['category']:
                        category = None
                    else:
                        name = article['item']['category'].get('name', None)
                        required = article['item']['category'].get('required', False)
                        category = ItemArticleCategoryEnum.objects.filter(name=name, required=required).first()
                    
                    print(f"{article=}")
                    
                    ean13 = article['item'].get('ean13', 0)
                    
                    if article['item'].get('brand', {}).get('id', None):
                        brand = ItemArticleBrandEnum.objects.filter(**article['item']['brand'])
                    else:
                        brand = None
                    
                    group =  ItemArticleGroupEnum.objects.get_or_create(name=article['item']['group']['name'])[0] if article['item']['group'] else None
                    attachement = AttachementImageArticle.objects.filter(id=article['item']['attachement']['id']).first() if article['item']['attachement'] else None
                    
                    item = ItemArticle.objects.get_or_create(
                        name=article['item']['name'], ident=article['item']['ident'], category=category, group=group, attachement=attachement,
                        ean13=ean13, brand=brand
                    )
                    
                    tdc_article = Article( api_key=api_key, tdc=new_tdc[0], remise=article['remise'], quantity=article['quantity'], price=article['price'], item=item[0] )
                    tdc_article.save()
                    
        except Exception as e:
            return {'error': str(e)}, status.HTTP_400_BAD_REQUEST
        else:
            new_tdc = TicketDeCaisse.objects.get(api_key=api_key, id=new_tdcId)
            new_tdc.articles = Article.objects.filter(tdc=new_tdc)
            datas = TicketDeCaisseSerializer(new_tdc)
            return datas.data, status.HTTP_201_CREATED
