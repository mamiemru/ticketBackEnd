
import os

from configparser import ConfigParser

from django.conf import settings
from rest_framework import status
from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from rest_framework_api_key.models import APIKey

from ticket.service.mlService import MLService
from ticket.service.ticketdecaisseService import TicketDeCaisseService

FILE_SUFFIX_IS_IMAGE = ('.PNG', '.JPG', '.JPEG')

class Command(BaseCommand):
    help = "Auto push tdcs (but require to be manually validated)"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        user_config = ConfigParser()
        user_config.read(settings.USER_CONFIGURATION)
        
        if not user_config.get('CREDENTIALS', 'API_KEY'):
            raise CommandError('USER_CONFIGURATION file require section nammed CREDENTIALS with non empty API_KEY field')
        
        for file_name in os.listdir(settings.QUEUE_FOLDER_PATH):
            file_path = settings.QUEUE_FOLDER_PATH / file_name
            self.stdout.write(str(file_path))
            
            if file_path.suffix.upper() in FILE_SUFFIX_IS_IMAGE:
                
                datas = {
                    'image': File(open(file_path, 'rb'), name=file_name),
                    'type': 'unnammed', 
                    'category': 'ticket'
                }
                
                api_key = APIKey.objects.get_from_key(user_config.get('CREDENTIALS', 'API_KEY'))
                
                response, status_code = MLService.create(
                    datas=datas,
                    raw_api_key=user_config.get('CREDENTIALS', 'API_KEY'),
                    api_key=api_key
                )
                
                if status_code != status.HTTP_200_OK:
                    raise CommandError(f"{status_code=} {response=}")
                
                response['need_to_be_validated'] = True
                
                response, status_code = TicketDeCaisseService.create(
                    api_key=api_key,
                    tdc=response
                )
                
                if status_code != status.HTTP_201_CREATED:
                    raise CommandError(f"{status_code=} {response=}")
                self.stdout.write(f"{status_code=} {response=}")
                