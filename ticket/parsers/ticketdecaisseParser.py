
import json

from rest_framework.parsers import BaseParser

from ticket.models import *
from ticket.serializers import *

class TicketDeCaisseParser(BaseParser):
    
    media_type = 'application/json'

    def parse(self, stream, media_type=None, parser_context=None):
        
        json_request = json.loads(stream.read())
        
        json_shop = json_request.get('shop')
        
        shop = TicketDeCaisseShopEnum.objects.get_or_create(name=json_shop.get('name'))
        
        print(shop)
        
        tdc = TicketDeCaisse(**json_request)
        
        print(tdc)
        
        return None