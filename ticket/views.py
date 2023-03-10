
import os
import re
import datetime
import mimetypes
from calendar import monthrange

from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from django.http import HttpResponse

from wsgiref.util import FileWrapper

from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from ticket.service.dateService import DateService
from ticket.service.feuillesService import FeuillesService

from ticket.pagination import StandardResultsSetPagination

from .models import *
from .structs import ApexChart, ApexChartSerie
from .serializers import *

class TicketDeCaisseTypeEnumViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    serializer_class = TicketDeCaisseTypeEnumSerializer
    queryset = TicketDeCaisseTypeEnum.objects.all()
    
class ItemArticleCategoryEnumViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    serializer_class = ItemArticleCategoryEnumSerializer
    queryset = ItemArticleCategoryEnum.objects.all()
    
class TicketDeCaisseShopEnumViewSet(viewsets.ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    serializer_class = TicketDeCaisseShopEnumSerializer
    queryset = TicketDeCaisseShopEnum.objects.all()
    
class TicketDeCaisseLocalisationEnumViewSet(viewsets.ViewSet):
    
    def list(self, request, format=None):
        return Response(data=[], status=status.HTTP_200_OK)
    
class ItemArticleGroupEnumViewSet(viewsets.ModelViewSet):
    serializer_class = ItemArticleGroupEnumSerializer
    queryset = ItemArticleGroupEnum.objects.all()
    
class ItemArticleViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    parser_classes = [JSONParser]
    serializer_class = ItemArticleSerializer
    queryset = ItemArticle.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def update(self, request, pk, format=None):
        itemarticle = request.data
        required = itemarticle['category'].get('required', False)
        category = ItemArticleCategoryEnum.objects.get_or_create(name=itemarticle['category']['name'], required=required)[0]
        group =  ItemArticleGroupEnum.objects.get_or_create(name=itemarticle['group']['name'])[0] if itemarticle['group'] else None
        attachement = AttachementImageArticle.objects.filter(id=itemarticle['attachement']['id']).first() if itemarticle['attachement'] else None
        item = ItemArticle.objects.get(id=itemarticle['id'])
        item.name = itemarticle['name']
        item.ident = itemarticle['ident']
        item.category = category
        item.group = group
        item.attachement = attachement
        item.save()
        datas = ItemArticleSerializer(item)
        return Response(data=datas.data, status=status.HTTP_200_OK)
    
class ItemArticleFilterViewSet(ListModelMixin, viewsets.GenericViewSet):
    parser_classes = [JSONParser]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def list(self, request, format=None):
        
        print(request.data)
        
        ident = request.data.get('item', {}).get('ident', None)
        category = request.data.get('item', {}).get('category', {}).get('name', None)
        group = request.data.get('item', {}).get('group', {}).get('name', None)
        tdcshop = request.data.get('tdc', {}).get('shop', {}).get('name', None)
        tdccategory = request.data.get('tdc', {}).get('category', {}).get('name', None)
        
        articles = Article.objects
        if ident:
            articles = articles.filter(item__ident__icontains=ident.lower())
        if category:
            articles = articles.filter(item__category__name__icontains=category.lower())
        if group:
            articles = articles.filter(item__group__name__icontains=group.lower())
        if tdcshop:
            articles = articles.filter(tdc__shop__name__icontains=tdcshop.lower())
        if tdccategory:
            articles = articles.filter(tdc__category__name__icontains=tdccategory.lower())
            
        itemArticles_ids = articles.values_list('item', flat=True).all()
        itemArticles = ItemArticle.objects.filter(id__in=itemArticles_ids).all()
        datas = ItemArticleSerializer(itemArticles, many=True)
        
        '''
        pagination = StandardResultsSetPagination()
        paginate_qs = pagination.paginate_queryset(datas.data, request)
        return pagination.get_paginated_response(paginate_qs)
        '''
        return Response(data={"results": datas.data})
    
class TicketDeCaisseViewSet(viewsets.ModelViewSet):
    serializer_class = TicketDeCaisseSerializer
    queryset = TicketDeCaisse.objects.all()
    
    def retrieve(self, request, pk, format=None):
        tdc = TicketDeCaisse.objects.get(id=pk)
        tdc.articles = Article.objects.filter(tdc=pk)
        datas = TicketDeCaisseSerializer(tdc)
        return Response(datas.data)
    
    def list(self, request, last_n, format=None):
        last_n = min(last_n, len(TicketDeCaisse.objects.all()))
        results = TicketDeCaisse.objects.all().order_by('-date')[:last_n]
        datas = TicketDeCaisseSerializer(results, many=True)
        return Response(datas.data)  

class TicketDeCaisseViewSetCustomParser(viewsets.ModelViewSet):
    parser_classes = [JSONParser]
    serializer_class = TicketDeCaisseSerializer
    queryset = TicketDeCaisse.objects.all()
    
    def create(self, request, format=None):
        
        tdcId = None
        try:
            with transaction.atomic():
                tdc_date = DateService.dateStrToDateEnglishDateFormat(request.data['date'])
                
                print(f"{tdc_date=}")
                
                tdc_shop : TicketDeCaisseShopEnum = TicketDeCaisseShopEnum(**request.data['shop'])
                if tdc_shop.ident and tdc_shop.id:
                    tdc_shop = TicketDeCaisseShopEnum.objects.filter(
                        id=tdc_shop.id, ident=tdc_shop.ident, name=tdc_shop.name, city=tdc_shop.city, localisation=tdc_shop.localisation
                    ).first()
                else:
                    tdc_shop.ident = tdc_shop.name
                    tdc_shop.save()
                print(f"{tdc_shop=}")
                
                tdc_category = TicketDeCaisseTypeEnum.objects.get_or_create(**request.data['category'])[0]
                print(f"{tdc_category=}")
                
                if not tdc_category or not tdc_shop or not tdc_date:
                    return Response(data={'error': 'field empty'}, status=status.HTTP_400_BAD_REQUEST)
                
                if request.data['attachement']:
                    tdc_attachement = AttachementImageTicket.objects.filter(id=request.data['attachement']['id']).first()
                else:
                    tdc_attachement = None
                print(f"{tdc_attachement=}")
                
                tdc = TicketDeCaisse.objects.get_or_create(shop=tdc_shop, category=tdc_category, date=tdc_date, attachement=tdc_attachement)
                if not tdc[1]:
                    raise Exception("Ticket de caisse already exists")
                tdcId = tdc[0].id
                print(tdc, tdcId)
                
                for article in request.data['articles']:
                    if not article['item'] or not article['item']['category']:
                        raise Exception("one field is empty")
                    
                    required = article['item']['category'].get('required', False)
                    category = ItemArticleCategoryEnum.objects.get_or_create(name=article['item']['category']['name'], required=required)[0]
                    print(category)
                    group =  ItemArticleGroupEnum.objects.get_or_create(name=article['item']['group']['name'])[0] if article['item']['group'] else None
                    print(group)
                    attachement = AttachementImageArticle.objects.filter(id=article['item']['attachement']['id']).first() if article['item']['attachement'] else None
                    print(attachement)
                    item = ItemArticle.objects.get_or_create(
                        name=article['item']['name'], ident=article['item']['ident'], category=category, group=group, attachement=attachement
                    )
                    print(item)
                    
                    tdc_article = Article( tdc=tdc[0], remise=article['remise'], quantity=article['quantity'], price=article['price'], item=item[0] )
                    tdc_article.save()
                    print(tdc_article)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
               
        new_tdc = TicketDeCaisse.objects.get(id=tdcId)
        new_tdc.articles = Article.objects.filter(tdc=new_tdc)
        datas = TicketDeCaisseSerializer(new_tdc)
        return Response(data=datas.data, status=status.HTTP_201_CREATED)
    
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    
    def list(self, request, format=None):
        article_item_ident = request.GET.get('ident', None)
        
        if article_item_ident is None:
            return Response(data={"error": "missing or bad url param ?ident="}, status=status.HTTP_400_BAD_REQUEST)
        
        articles = Article.objects.filter(item__ident=article_item_ident).all()
        
        if not articles:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        datas = ArticleSerializer(articles, many=True)
        return Response(datas.data, status=status.HTTP_200_OK)
    
class FeuilleViewSet(viewsets.ModelViewSet):
    serializer_class = FeuilleSerializer
    queryset = Feuille.objects.all()
    
    def retrieve(self, request, pk, format=None):
        feuille = FeuillesService.retrieve(pk)
        datas = FeuilleSerializer(feuille)
        return Response(datas.data)
    
    def list(self, request, format=None):
        FeuillesService.check_new_month()
        feuille = Feuille.objects.all().values('date', 'id')
        datas = FeuilleSerializer(feuille, many=True)
        return Response(datas.data)
    
class FeuilleTableViewSet(APIView):
    
    def get(self, request, pk, format=None):
        feuille = FeuillesService.retrieve(pk)
        table   = FeuillesService.feuilleToDataTable(feuille)
        return Response(table.to_json())
        
class FeuilleSummaryViewSet(APIView):
    
    def get(self, request, pk, format=None):
        feuille = FeuillesService.retrieve(pk)
        table   = FeuillesService.feuilleToDataTable(feuille)
        summary = FeuillesService.feuilleSummary(feuille, table)
        datas   = FeuilleSummarySerializer(summary)
        return Response(datas.data)
    
class CompletionChangedViewSet(APIView):
    
    def get(self, request, format=None):
        datas = CompletionChangedSerilizer()
        return Response(datas.data)
    
class CompletionChangedShopViewSet(APIView):
    
    def get(self, request, shop, format=None):
        shopObj   = TicketDeCaisseShopEnum.objects.filter(name=shop).first()
        
        if not shopObj:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        articlesQuery = Article.objects.filter(tdc__shop=shopObj)
        
        data_keys = { 
            'tdc_category': 'tdc__category__name',
            'item_ident': 'item__ident',
            'item_category': 'item__category__name',
            'item_name': 'item__name',
            'item_group': 'item__group__name'
        }
        
        datas = {
            k: [l[v] for l in articlesQuery.values(v).distinct().order_by(v)] for k,v in data_keys.items()
        }
        
        datas['tdc'] = TicketDeCaisseShopEnumSerializer(shopObj).data
        datas['quant'] = 1
        datas['remise'] = 0.0
        
        return Response(data=datas, status=status.HTTP_200_OK)
    
class CompletionChangedArticleItemIdentViewSet(APIView):
    
    def get(self, request, shop, ident, format=None):
        shopObj   = TicketDeCaisseShopEnum.objects.filter(name=shop).first()
        
        if not shopObj:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        article = Article.objects.filter(Q(tdc__shop=shopObj), Q(item__ident=ident)).last()
        
        if not article:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
            
        article.item.attachement = AttachementImageArticle.objects.filter(name=ident).first()
        datas = ArticleSerializer(article)
        return Response(data=datas.data)
    
class PlotMonthGraph(viewsets.ViewSet):
    
    def plotM(self, request, feuille_id, format=None):
        
        feuille = Feuille.objects.get(id=feuille_id)
        
        if not feuille:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        date = datetime.datetime.fromtimestamp(feuille.date)
        tdcs = FeuillesService.retrieve_tdcs(pk=feuille_id)
        mapping = range(1,monthrange(date.year, date.month)[1]+1)
                
        total_per_day : Dict[str, float] = dict()
        for tdc in tdcs:
            if tdc.date.day in total_per_day:
                total_per_day[tdc.date.day] += tdc.total()
            else:
                total_per_day[tdc.date.day] = tdc.total()
            
        def __v(c):
            return round(c,2) if type(c) == float else c
        
        datas = ApexChart.to_type_column(
            x=list(mapping), 
            series=[ApexChartSerie(name="total", type="column", data=[__v(total_per_day.get(x, 0.0)) for x in mapping])], 
            title_text=f"Somme d'argent d??pens??e au {date.month} {date.year}"
        )
        
        return Response(data=datas, status=status.HTTP_200_OK)
    
    def plotS(self, request, feuille_id, format=None):
        feuille = Feuille.objects.get(id=feuille_id)
        
        if not feuille:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        date = datetime.datetime.fromtimestamp(feuille.date)
        tdcs = FeuillesService.retrieve_tdcs(pk=feuille_id)
        
        shops_label = list()
        shops_quant = list()
        
        for tdc in tdcs:
            try:
                index = shops_label.index(tdc.shop.name)
            except:
                shops_label.append(tdc.shop.name)
                shops_quant.append(1)
            else:
                shops_quant[index] += 1
                
        datas = ApexChart.to_type_column(
            x=shops_label, 
            series=[ApexChartSerie(name="occurance", type="column", data=shops_quant)], 
            title_text=f"Magasins pendant {date.month} {date.year}"
        )
        
        print(datas)
        
        return Response(data=datas, status=status.HTTP_200_OK)
        
class Attachements(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AttachementsImagesSerializer
    queryset = AttachementsImages.objects.all()
    
    def retrieve(self, request, category, filename, format=None):
        img = AttachementsImages.objects.filter(name=filename, category=category).first()
        
        if not img:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)

        datas = AttachementsImagesSerializer(img)
        return Response(data=datas.data, status=status.HTTP_200_OK)
    
    def create(self, request, format=None):
        image = request.data.get('image', None)
        name = request.data.get('name', None)
        category = request.data.get('category', None)
        
        if image is None or category is None:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        
        if not name:
            name = image.namme
        
        if category == 'article':
            img = AttachementImageArticle.objects.create(image=image, name=name, category='article')
            datas = AttachementImageArticleSerializer(img)
            return Response(data=datas.data, status=status.HTTP_201_CREATED)
        elif category == 'ticket':
            img = AttachementImageTicket.objects.create(image=image, name=name, category='ticket')
            datas = AttachementImageTicketSerializer(img)
            return Response(data=datas.data, status=status.HTTP_201_CREATED)

        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

class TicketML(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AttachementsImagesSerializer
    
    def create(self, request, format=None):
        image = request.data.get('image', None)
        typ = request.data.get('type', None)
        category = request.data.get('category', None)
        
        if image is None or category is None:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if category == 'ticket':
                
                if typ is None:
                    return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
                
                minioModel = AttachementImageTicket(name=image.name, type=typ, image=image)
                minioModel.save()
                serializerMinioModel = AttachementImageTicketSerializer(minioModel)
            else:
                minioModel = AttachementImageArticle(name=image.name, image=image)
                minioModel.save()
                serializerMinioModel = AttachementImageArticleSerializer(minioModel)
                
        except FileExistsError as e:
            return Response(data=None, status=status.HTTP_409_CONFLICT)
        else:
            import requests
            datas = requests.post(
                f"http://localhost:8001/to_ticket_de_caisse/{serializerMinioModel.data['id']}/",
                headers={ 'Content-Type': 'application/json' }
            )
            
            ## update image name in Model and in Minio (use date & user)
            
            if datas.status_code == status.HTTP_200_OK:
                return Response(data=datas.json(), status=status.HTTP_201_CREATED)
            
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
