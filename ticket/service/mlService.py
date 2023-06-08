
import requests
from typing import Dict
from rest_framework import status
from rest_framework_api_key.models import AbstractAPIKey
from ticket.models import AttachementImageTicket

class MLService:
    
    @staticmethod
    def create(api_key: AbstractAPIKey, datas : Dict[str, str], raw_api_key: str):
        image = datas.get('image', None)
        typ = datas.get('type', None)
        category = datas.get('category', None)
        
        print(f"{typ=}, {category=}")
        
        if image is None or category is None:
            return 'image or category is null', status.HTTP_400_BAD_REQUEST
        
        ## TODO update image name in Model and in Minio (use date & user)
        
        if category == 'ticket': ## to ensure this is not an article image
            
            check_already_exist = AttachementImageTicket.objects.filter(api_key=api_key, name=image.name).first()
            
            if not check_already_exist:
                try:
                    attachement_object = AttachementImageTicket(api_key=api_key, name=image.name, type=typ, image=image)
                    attachement_object.save()
                except FileExistsError:
                    return {'error': f'the file {image.name} already exist'}, status.HTTP_409_CONFLICT
                
            try:
                attachement_object = AttachementImageTicket.objects.get(api_key=api_key, name=image.name)
            except:
                return {'error': 'could not get attachement'}, status.HTTP_409_CONFLICT
            else:        
                datas = requests.post(
                    f"http://localhost:8001/to_ticket_de_caisse/{attachement_object.id}/",
                    headers={ 
                        'Content-Type': 'application/json',  
                        'Authorization': f'Api-Key {raw_api_key}'
                    }
                )
                if status.HTTP_200_OK <= datas.status_code <= status.HTTP_201_CREATED:
                    response = datas.json()
                    
                    print(response)
                    
                    if attachement_object.type == 'unnammed':
                        attachement_object.type = response.get('type', attachement_object.type)
                        attachement_object.save()
                    
                    return response, status.HTTP_200_OK
                
                if datas.status_code == status.HTTP_403_FORBIDDEN:
                    return None, status.HTTP_403_FORBIDDEN
                
                return None, status.HTTP_400_BAD_REQUEST
        
        return category, status.HTTP_400_BAD_REQUEST     