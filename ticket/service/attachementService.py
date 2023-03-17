
from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.models import AttachementsImages
from ticket.models import AttachementImageTicket
from ticket.models import AttachementImageArticle

from ticket.serializers import AttachementImageTicketSerializer
from ticket.serializers import AttachementImageArticleSerializer

class AttachementService:
    
    @staticmethod
    def retrieve(api_key: APIKey, category: str, filename: str):
        img = AttachementsImages.objects.filter(name=filename, category=category).first()
        
        if not img:
            return None, status.HTTP_404_NOT_FOUND

        datas = AttachementsImagesSerializer(img)
        return datas.data, status.HTTP_200_OK
    
    @staticmethod
    def create(api_key: APIKey, data):
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
            img = AttachementImageTicket.objects.create(image=image, name=name, category='ticket')
            datas = AttachementImageTicketSerializer(img)
            return datas.data, status.HTTP_201_CREATED

        return None, status.HTTP_400_BAD_REQUEST