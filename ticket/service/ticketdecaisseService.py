import json

from typing import Dict
from typing import Tuple
from typing import Union

from django.db import transaction

from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.service.dateService import DateService

from ticket.models import Article
from ticket.models import ItemArticle
from ticket.models import ShopEnseigne
from ticket.models import TicketDeCaisse
from ticket.models import ItemArticleToGS1
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
    def __get_tdc_date(date) -> str:
        return DateService.dateStrToDateEnglishDateFormat(date) if date else None
    
    @staticmethod
    def __process_tdc_shop_and_enseigne_or_none(in_request_tdc_shop: Dict[str, any]) -> TicketDeCaisseShopEnum:
        tdc_shop_enseigne = in_request_tdc_shop.pop('enseigne') ## pop the enseigne key is mandatory here
        
        tdc_shop : TicketDeCaisseShopEnum = TicketDeCaisseShopEnum(**in_request_tdc_shop)
        tdc_shop.enseigne = ShopEnseigne(**tdc_shop_enseigne) if tdc_shop_enseigne else None
        
        if tdc_shop.valide and tdc_shop.id:
            tdc_shop = TicketDeCaisseShopEnum.objects.filter(
                id=tdc_shop.id, ident=tdc_shop.ident, name=tdc_shop.name, city=tdc_shop.city, localisation=tdc_shop.localisation
            ).first()
        else:
            tdc_shop.valide = True
            tdc_shop.save()
        
        return tdc_shop
    
    @staticmethod
    def __get_tdc_attachement_by_id_or_args_or_none(in_request_tdc_attachement: Dict[str, str]) -> Union[AttachementImageTicket, None]:
        if in_request_tdc_attachement:
            if 'id' in in_request_tdc_attachement:
                return AttachementImageTicket.objects.get(id=in_request_tdc_attachement['id'])
            else:
                return AttachementImageTicket.objects.filter(**in_request_tdc_attachement).first()
        return None
    
    @staticmethod
    def __get_brand_by_any_way_or_none(in_request_brand: Dict[str, any]) -> Union[ItemArticleBrandEnum, None]:
        if in_request_brand:
            if type(in_request_brand) is int:
                return ItemArticleBrandEnum.objects.get(pk=in_request_brand)
            elif 'name' in in_request_brand:
                return ItemArticleBrandEnum.get_brand_by_name_or_none(in_request_brand)
        return None
    
    @staticmethod
    def create(api_key: APIKey, tdc: Dict):
        """ Perform checks and save a new TicketDeCaisse.
            For now, Any ItemArticles can be overwritten.

        Args:
            api_key (APIKey): APIKey
            tdc (Dict): json serialized TicketDeCaisse

        Raises:
            Exception, 500: consistancy errors

        Returns:
            TicketDeCaisse, 201: tdc is succesfully saved
            Dict, 400: see 'error' key
        """
        
        new_tdcId = None
        try:
            with transaction.atomic():
                tdc_date : str = TicketDeCaisseService.__get_tdc_date(tdc['date'])
                tdc_shop : TicketDeCaisseShopEnum = TicketDeCaisseService.__process_tdc_shop_and_enseigne_or_none(tdc['shop'])
                tdc_category : TicketDeCaisseTypeEnum = TicketDeCaisseTypeEnum.get_or_create_tdc_type_by_args(tdc['category'])
                tdc_shop_enseigne : ShopEnseigne = tdc_shop.enseigne
                
                tdc_type : str = tdc['type']
                tdc_total : float = round(tdc['total'], 2)
                tdc_remise : float = tdc.get('remise', 0.0)
                tdc_need_to_be_validated = tdc.get('need_to_be_validated', True)
                
                if not tdc_category or not tdc_shop or not tdc_date or not tdc_type or not tdc_total:
                    return {'error': 'mandatory field empty'}, status.HTTP_400_BAD_REQUEST
                
                tdc_attachement = TicketDeCaisseService.__get_tdc_attachement_by_id_or_args_or_none(tdc['attachement'])
                new_tdc, new_tdc_added = TicketDeCaisse.objects.get_or_create(
                    api_key=api_key, shop=tdc_shop, category=tdc_category, date=tdc_date, attachement=tdc_attachement, 
                    type=tdc_type, total=tdc_total, remise=tdc_remise, need_to_be_validated=tdc_need_to_be_validated
                )
                
                new_tdcId : int = new_tdc.id
                if not new_tdc_added or not new_tdcId:
                    return {'error': 'An other TDC with same constraints already exist' }, status.HTTP_409_CONFLICT
                
                for article in tdc['articles']:
                    ## start for one article ##
                    if not article['item']:
                        raise Exception("one Item field is empty")
                    
                    ident = article['item']['ident']
                    
                    ''' wtf those lines?
                    if tdc_type == 'receipece' and not article['item']['category']:
                        category = None
                    else:
                    '''
                    
                    ean13 = article['item'].get('ean13', 0)
                    name = article['item'].get('name', ident)
                    brand = TicketDeCaisseService.__get_brand_by_any_way_or_none(article['item'].get('brand', None))
                    category = ItemArticleCategoryEnum.get_ia_category_by_name_or_none(article['item']['category'].get('name', None))
                    group =  ItemArticleGroupEnum.get_group_by_name_or_none(article['item']['group'])
                    attachement = AttachementImageArticle.get_attachement_by_id_or_none(article['item']['attachement'])
                    item = ItemArticle.objects.filter(ident=ident).last()
                        
                    print(f"{ident=}, {name=}, {category=} {brand=} {group=}")
                    if not item:
                        item = ItemArticle(name=name, ident=ident, category=category, group=group, attachement=attachement, ean13=ean13, brand=brand)
                        item.save()
                        
                    ## only exist in order to overwrite fields if empty/null/0
                    if (not item.ean13 or item.ean13 == 0) and ean13:
                        item.ean13 = ean13
                        item.save()
                    if not item.attachement and attachement:
                        item.attachement = attachement
                        item.save()
                    if not item.brand and brand:
                        item.brand = brand
                        item.save()
                    
                    tdc_article = Article( api_key=api_key, tdc=new_tdc, remise=article['remise'], quantity=article['quantity'], price=article['price'], item=item )
                    tdc_article.save()
                    
                    if ean13 and tdc_shop_enseigne and ident and ItemArticleToGS1.objects.filter(ident=ident, ean13=ean13, shop=tdc_shop, enseigne=tdc_shop_enseigne).count == 0:
                        iags1 = ItemArticleToGS1(ident=ident, ean13=ean13, shop=tdc_shop, enseigne=tdc_shop_enseigne)
                        iags1.save()
                    ## end for one article ##
                    
        except Exception as e:
            return {'error': str(e)}, status.HTTP_400_BAD_REQUEST
        else:
            new_tdc = TicketDeCaisse.objects.get(api_key=api_key, id=new_tdcId)
            new_tdc.articles = Article.objects.filter(tdc=new_tdc)
            datas = TicketDeCaisseSerializer(new_tdc)
            return datas.data, status.HTTP_201_CREATED
