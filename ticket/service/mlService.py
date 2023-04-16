
import requests
from typing import Dict
from rest_framework import status
from rest_framework_api_key.models import AbstractAPIKey
from ticket.models import AttachementImageTicket

class MLService:
    
    @staticmethod
    def create(api_key: AbstractAPIKey, data : Dict[str, str], raw_api_key: str):
        image = data.get('image', None)
        typ = data.get('type', None)
        category = data.get('category', None)
        
        if image is None or category is None:
            return 'image or category is null', status.HTTP_400_BAD_REQUEST
        
        ## TODO update image name in Model and in Minio (use date & user)
        
        if category == 'ticket':
            if typ is None:
                return 'type is null', status.HTTP_400_BAD_REQUEST
            
            check_already_exist = AttachementImageTicket.objects.filter(api_key=api_key, name=image.name, type=typ).first()
            
            if not check_already_exist:
                try:
                    minioModel = AttachementImageTicket(api_key=api_key, name=image.name, type=typ, image=image)
                    minioModel.save()
                except FileExistsError:
                    return None, status.HTTP_409_CONFLICT
                
            try:
                minioModel = AttachementImageTicket.objects.get(api_key=api_key, name=image.name)
            except:
                return None, status.HTTP_409_CONFLICT
            else:        
                datas = requests.post(
                    f"http://localhost:8001/to_ticket_de_caisse/{minioModel.id}/",
                    headers={ 
                        'Content-Type': 'application/json',  
                        'Authorization': f'Api-Key {raw_api_key}'
                    }
                )
                if status.HTTP_200_OK <= datas.status_code <= status.HTTP_201_CREATED:
                    return datas.json(), status.HTTP_201_CREATED
                
                if datas.status_code == status.HTTP_403_FORBIDDEN:
                    return None, status.HTTP_403_FORBIDDEN
                
                return None, status.HTTP_400_BAD_REQUEST    
        else:
            return category, status.HTTP_400_BAD_REQUEST     