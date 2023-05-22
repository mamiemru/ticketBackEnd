
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from rest_framework.parsers import JSONParser
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey

from ticket.service.mlService import MLService
from ticket.service.plotService import PlotService
from ticket.service.articleService import ArticleService
from ticket.service.feuillesService import FeuillesService
from ticket.service.completionService import CompletionService
from ticket.service.itemArticleService import ItemArticleService
from ticket.service.attachementService import AttachementService
from ticket.service.ticketdecaisseService import TicketDeCaisseService

from ticket.pagination import StandardResultsSetPagination

from .models import *
from .serializers import *


def get_raw_api_key(request):
    return request.META["HTTP_AUTHORIZATION"].split()[1]

def get_api_key(request):
    return APIKey.objects.get_from_key(get_raw_api_key(request=request))

class ApiKeyViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser, FormParser]
    
    def retrieve(self, request, format=None):
        print(request.META['HTTP_AUTHORIZATION'])
        api_key = get_api_key(request=request)
        print(f'{api_key=}')
        return Response(data=None , status=status.HTTP_200_OK if api_key else status.HTTP_403_FORBIDDEN)

class TicketDeCaisseTypeEnumViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser, FormParser]
    serializer_class = TicketDeCaisseTypeEnumSerializer
    queryset = TicketDeCaisseTypeEnum.objects.all()
    
class ItemArticleCategoryEnumViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser, FormParser]
    serializer_class = ItemArticleCategoryEnumSerializer
    queryset = ItemArticleCategoryEnum.objects.all()    

class ItemArticleBrandEnumViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser, FormParser]
    serializer_class = ItemArticleBrandEnumSerializer
    queryset = ItemArticleBrandEnum.objects.all()
    
class TicketDeCaisseShopEnumViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser, FormParser]
    serializer_class = TicketDeCaisseShopEnumSerializer
    queryset = TicketDeCaisseShopEnum.objects.all()
    
class TicketDeCaisseLocalisationEnumViewSet(viewsets.ViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser, FormParser]
    
    def list(self, request, format=None):
        return Response(data=[], status=status.HTTP_200_OK)
    
class ItemArticleGroupEnumViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser, FormParser]
    serializer_class = ItemArticleGroupEnumSerializer
    queryset = ItemArticleGroupEnum.objects.all()
    
class ItemArticleViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser]
    serializer_class = ItemArticleSerializer
    queryset = ItemArticle.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def update(self, request, pk, format=None):
        api_key = get_api_key(request=request)
        datas = ItemArticleService.update(api_key=api_key, item_article=request.data, pk=pk)
        return Response(data=datas.data, status=status.HTTP_200_OK)
    
class ItemArticleFilterViewSet(ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def list(self, request, format=None):
        api_key = get_api_key(request=request)
        data = ItemArticleService.list(api_key=api_key, item_article=request.data)
        return Response(data=data, status=status.HTTP_200_OK)
    
class TicketDeCaisseViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    serializer_class = TicketDeCaisseSerializer
    queryset = TicketDeCaisse.objects.all()
    
    def retrieve(self, request, pk, format=None):
        api_key = get_api_key(request=request)
        tdc = TicketDeCaisse.objects.get(id=pk, api_key=api_key)
        tdc.articles = Article.objects.filter(tdc=pk)
        datas = TicketDeCaisseSerializer(tdc)
        return Response(datas.data)
    
    def list(self, request, last_n, format=None):
        api_key = get_api_key(request=request)
        last_n = min(last_n, TicketDeCaisse.objects.filter(api_key=api_key).count())
        results = TicketDeCaisse.objects.filter(api_key=api_key).order_by('-date')[:last_n]
        datas = TicketDeCaisseSerializer(results, many=True)
        return Response(datas.data)  

class TicketDeCaisseViewSetCustomParser(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [JSONParser]
    serializer_class = TicketDeCaisseSerializer
    queryset = TicketDeCaisse.objects.all()
    
    def create(self, request, format=None):
        api_key = get_api_key(request=request)
        data, status = TicketDeCaisseService.create(api_key=api_key, tdc=request.data)
        return Response(data=data, status=status)
    
class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    
    def list(self, request, format=None):
        api_key = get_api_key(request=request)
        datas, status = ArticleService.list(api_key=api_key, article_item=request.GET)
        return Response(datas.data, status=status)
    
class FeuilleViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    serializer_class = FeuilleSerializer
    queryset = Feuille.objects.all()
    
    def retrieve(self, request, pk, format=None):
        api_key = get_api_key(request=request)
        feuille = FeuillesService.retrieve(api_key=api_key, pk=pk)
        datas = FeuilleSerializer(feuille)
        return Response(datas.data)
    
    def list(self, request, format=None):
        api_key = get_api_key(request=request)
        FeuillesService.check_new_month(api_key=api_key)
        feuille = Feuille.objects.filter(api_key=api_key).values('date', 'id')
        datas = FeuilleSerializer(feuille, many=True)
        return Response(datas.data)
    
class FeuilleTableViewSet(APIView):
    permission_classes = [HasAPIKey]
    
    def get(self, request, pk, format=None):
        api_key = get_api_key(request=request)
        feuille = FeuillesService.retrieve(api_key=api_key, pk=pk)
        table   = FeuillesService.feuilleToDataTable(feuille)
        return Response(table.to_json())
        
class FeuilleSummaryViewSet(APIView):
    permission_classes = [HasAPIKey]
    
    def get(self, request, pk, format=None):
        api_key = get_api_key(request=request)
        feuille = FeuillesService.retrieve(api_key=api_key, pk=pk)
        table   = FeuillesService.feuilleToDataTable(feuille)
        summary = FeuillesService.feuilleSummary(feuille, table)
        datas   = FeuilleSummarySerializer(summary)
        return Response(datas.data)
    
class CompletionChangedViewSet(APIView):
    permission_classes = [HasAPIKey]
    
    def get(self, request, format=None):
        datas = CompletionChangedSerilizer()
        return Response(datas.data)
    
class CompletionChangedShopViewSet(APIView):
    permission_classes = [HasAPIKey]
    
    def get(self, request, shop_id: int, format=None):
        api_key = get_api_key(request=request)
        data, status = CompletionService.get_changed_shop(api_key=api_key, shop_id=shop_id)
        return Response(data=data, status=status)
    
class CompletionChangedArticleItemIdentViewSet(APIView):
    permission_classes = [HasAPIKey]
    
    def get(self, request, shop_name, item_article_ident, format=None):
        api_key = get_api_key(request=request)
        data, status = CompletionService.get_changed_item_article(api_key=api_key, shop_name=shop_name, item_article_ident=item_article_ident)
        return Response(data=data, status=status)
    
class PlotMonthGraph(viewsets.ViewSet):
    permission_classes = [HasAPIKey]
    
    def plotM(self, request, feuille_id, format=None):
        api_key = get_api_key(request=request)
        data, status = PlotService.plotM(api_key=api_key, feuille_id=feuille_id)
        return Response(data=data, status=status)
    
    def plotS(self, request, feuille_id, format=None):
        api_key = get_api_key(request=request)
        data, status = PlotService.plotS(api_key=api_key, feuille_id=feuille_id)
        return Response(data=data, status=status)
        
class Attachements(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AttachementsImagesSerializer
    queryset = AttachementsImages.objects.all()
    
    def retrieve(self, request, category, filename, format=None):
        api_key = get_api_key(request=request)
        data, status = AttachementService.retrieve(api_key=api_key, category=category, filename=filename)
        return Response(data=data, status=status)
    
    def create(self, request, format=None):
        api_key = get_api_key(request=request)
        data, status = AttachementService.create(api_key=api_key, data=request.data)
        return Response(data=data, status=status)

class TicketML(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AttachementsImagesSerializer
    
    def create(self, request, format=None):
        api_key = get_api_key(request=request)
        raw_api_key = get_raw_api_key(request=request)
        data, status = MLService.create(api_key=api_key, data=request.data, raw_api_key=raw_api_key)
        return Response(data=data, status=status)