
import requests

class MLService:
    
    @staticmethod
    def create(api_key, data, format=None):
        serializerMinioModel = None
        image = data.get('image', None)
        typ = data.get('type', None)
        category = data.get('category', None)
        
        if image is None or category is None:
            return 'image or category is null', status.HTTP_400_BAD_REQUEST
        
        ## TODO update image name in Model and in Minio (use date & user)
        
        if category == 'ticket':
            if typ is None:
                return 'type is null', status.HTTP_400_BAD_REQUEST
            
            try:
                minioModel = AttachementImageTicket(name=image.name, type=typ, image=image)
                minioModel.save()
            except FileExistsError as e:
                print(f'file {image.name} already exist')
                minioModel = AttachementImageTicket.objects.get(name=image.name)
            
            serializerMinioModel = AttachementImageTicketSerializer(minioModel)
        else:
            try:
                minioModel = AttachementImageArticle(name=image.name, image=image)
                minioModel.save()
            except FileExistsError as e:
                print(f'file {image.name} already exist')
                minioModel = AttachementImageArticle.objects.get(name=image.name)
                
            serializerMinioModel = AttachementImageArticleSerializer(minioModel)
                
        datas = requests.post(
            f"http://localhost:8001/to_ticket_de_caisse/{serializerMinioModel.data['id']}/",
            headers={ 'Content-Type': 'application/json' }
        )
        
        if datas.status_code == status.HTTP_200_OK:
            return datas.json(), status.HTTP_201_CREATED
            
        return None, status.HTTP_400_BAD_REQUEST