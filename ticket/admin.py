from django.contrib import admin
from ticket.models import *

admin.site.register(TicketDeCaisseTypeEnum)
admin.site.register(TicketDeCaisseShopEnum)
admin.site.register(TicketDeCaisseLocalisationEnum)
admin.site.register(ItemArticleCategoryEnum)
admin.site.register(ItemArticleGroupEnum)
admin.site.register(ItemArticle)
admin.site.register(Article)
admin.site.register(TicketDeCaisse)
admin.site.register(Feuille)
admin.site.register(AttachementsImages)