import datetime
from calendar import monthrange

from rest_framework import status
from rest_framework_api_key.models import APIKey

from ticket.models import Feuille
from ticket.structs import ApexChart
from ticket.structs import ApexChartSerie

from ticket.service.feuillesService import FeuillesService

class PlotService:
    
    @staticmethod
    def plotM(api_key: APIKey, feuille_id: str):
        
        feuille = Feuille.objects.get(api_key=api_key, id=feuille_id)
        
        if not feuille:
            return None, status.HTTP_404_NOT_FOUND

        date = datetime.datetime.fromtimestamp(feuille.date)
        tdcs = FeuillesService.retrieve_tdcs(api_key=api_key, pk=feuille_id)
        mapping = range(1,monthrange(date.year, date.month)[1]+1)
                
        total_per_day : Dict[str, float] = dict()
        for tdc in tdcs:
            if tdc.date.day in total_per_day:
                total_per_day[tdc.date.day] += tdc.total
            else:
                total_per_day[tdc.date.day] = tdc.total
            
        def __v(c):
            return round(c,2) if type(c) == float else c
        
        datas = ApexChart.to_type_column(
            x=list(mapping), 
            series=[ApexChartSerie(name="total", type="column", data=[__v(total_per_day.get(x, 0.0)) for x in mapping])], 
            title_text=f"Somme d'argent dépensée au {date.month} {date.year}"
        )
        
        return datas, status.HTTP_200_OK
    
    @staticmethod
    def plotS(api_key: APIKey, feuille_id: str):
        feuille = Feuille.objects.get(api_key=api_key, id=feuille_id)
        
        if not feuille:
            return None, status.HTTP_404_NOT_FOUND
        
        date = datetime.datetime.fromtimestamp(feuille.date)
        tdcs = FeuillesService.retrieve_tdcs(api_key=api_key, pk=feuille_id)
        
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
        
        return datas, status.HTTP_200_OK
