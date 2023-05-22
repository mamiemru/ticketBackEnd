
from typing import Dict

from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.models import AttachementsImages
from ticket.models import AttachementImageTicket
from ticket.models import AttachementImageArticle
from ticket.serializers import AttachementsImagesSerializer
from ticket.serializers import AttachementImageTicketSerializer
from ticket.serializers import AttachementImageArticleSerializer

class AttachementService:
    
    @staticmethod
    def retrieve(api_key: APIKey, category: str, filename: str):
        """ Return the first AttachementsImages with name and category respectivly equal to filename and category parameters

        Args:
            api_key (APIKey): APIKey
            category (str): category
            filename (str): filename

        Returns:
            AttachementsImages, 200: found
            None, 404: otherwise
        """
        
        img = AttachementsImages.objects.filter(name=filename, category=category).first()
        
        if not img:
            return None, status.HTTP_404_NOT_FOUND

        datas = AttachementsImagesSerializer(img)
        return datas.data, status.HTTP_200_OK
    
    @staticmethod
    def create(api_key: APIKey, data: Dict):
        """ Create and save an ImageObject (Attachement) using name, image and category field from data parameter

        Args:
            api_key (APIKey): _description_
            data (Dict): Dict containing name, image and category keys acessible using get method

        Returns:
            AttachementImageArticle, 201: if category is 'article'
            AttachementImageTicket, 201: if category is 'ticket'
            None, 400: otherwise
        """
        
        name = data.get('name', None)
        image = data.get('image', None)
        category = data.get('category', None)
        
        if image is None or category is None:
            return None, status.HTTP_400_BAD_REQUEST
        
        if not name:
            name = image.namme
        
        if category == 'article':
            img = AttachementImageArticle.objects.create(image=image, name=name, category='article')
            datas = AttachementImageArticleSerializer(img)
            return datas.data, status.HTTP_201_CREATED
        elif category == 'ticket':
            img = AttachementImageTicket.objects.create(api_key=api_key, image=image, name=name, category='ticket')
            datas = AttachementImageTicketSerializer(img)
            return datas.data, status.HTTP_201_CREATED

        return None, status.HTTP_400_BAD_REQUEST