"""ticketBackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import re_path
from django.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from ticket.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/check/', ApiKeyViewSet.as_view({'get': 'retrieve'})),
    path('ticket_de_caisse/category/', TicketDeCaisseTypeEnumViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ticket_de_caisse/category/<str:pk>/', TicketDeCaisseTypeEnumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('ticket_de_caisse/article/item/category/', ItemArticleCategoryEnumViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ticket_de_caisse/article/item/category/<str:pk>/', ItemArticleCategoryEnumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('ticket_de_caisse/shop/', TicketDeCaisseShopEnumViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ticket_de_caisse/shop/<int:pk>/', TicketDeCaisseShopEnumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('ticket_de_caisse/shop/enseigne/', TicketDeCaisseShopEnseigneEnumViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ticket_de_caisse/shop/enseigne/<int:pk>/', TicketDeCaisseShopEnseigneEnumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('ticket_de_caisse/localisation/', TicketDeCaisseLocalisationEnumViewSet.as_view({'get': 'list'})),
    ## path('ticket_de_caisse/localisation/<str:pk>/', TicketDeCaisseLocalisationEnumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('ticket_de_caisse/article/item/group/', ItemArticleGroupEnumViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ticket_de_caisse/article/item/group/<str:pk>/', ItemArticleGroupEnumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('ticket_de_caisse/article/item/brand/', ItemArticleBrandEnumViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ticket_de_caisse/article/item/brand/<str:pk>/', ItemArticleBrandEnumViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('ticket_de_caisse/article/item/', ItemArticleViewSet.as_view({'get': 'list'})),
    path('ticket_de_caisse/article/item/filter/', ItemArticleFilterViewSet.as_view({'post': 'list'})),
    path('ticket_de_caisse/article/item/<str:pk>/', ItemArticleViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('ticket_de_caisse/last_n/<int:last_n>/', TicketDeCaisseViewSet.as_view({'get': 'list'})),
    path('ticket_de_caisse/article/', ArticleViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ticket_de_caisse/article/<str:pk>/', ArticleViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('ticket_de_caisse/article/ean13/<str:code>', ArticleViewSetEan13.as_view({'get': 'retrieve'})),
    path('ticket_de_caisse/', TicketDeCaisseViewSetCustomParser.as_view({'post': 'create'})),
    path('ticket_de_caisse/<str:pk>/', TicketDeCaisseViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('feuille/', FeuilleViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('feuille/<str:pk>/', FeuilleViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    path('feuille/monthly/<str:pk>/table/', FeuilleTableViewSet.as_view()),
    path('feuille/monthly/<str:pk>/summary/', FeuilleSummaryViewSet.as_view()),
    path('feuille/monthly/<int:feuille_id>/plot/', PlotMonthGraph.as_view({'get': 'plotM'})),
    path('feuille/monthly/<int:feuille_id>/plot/shop/', PlotMonthGraph.as_view({'get': 'plotS'})),
    path('completion/changed/', CompletionChangedViewSet.as_view()),
    path('completion/changed/<int:shop_id>/', CompletionChangedShopViewSet.as_view()),
    path('completion/changed/<str:shop_name>/article/item/<str:item_article_ident>/', CompletionChangedArticleItemIdentViewSet.as_view()),
    path('attachements/<str:category>/<str:filename>/', Attachements.as_view({ 'get': 'retrieve' })),
    path('attachements/', Attachements.as_view({ 'post': 'create' })),
    path('detection/', TicketML.as_view({ 'post': 'create' })),
    path('ml/attachement/ticket/', MlAttachementTicketViewSet.as_view({'get': 'list'})),
    path('ml/attachement/ticket/<str:pk>/', MlAttachementTicketViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    
    path('exo3/profil', ProfilViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('exo3/profil/<str:pk>', ProfilViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)