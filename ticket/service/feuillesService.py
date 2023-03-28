

import datetime

from typing import Dict
from dateutil.relativedelta import relativedelta

from ticket.models import Feuille
from ticket.models import Factures
from ticket.models import TicketDeCaisse

from ticket.structs import TableFeuille
from ticket.structs import TableFeuilleCategory

from ticket.service.dateService import DateService

from rest_framework_api_key.models import APIKey

class FeuillesService():
    """ Everything related to Feuille structure
    """
    
    @staticmethod
    def check_new_month(api_key):
        """ Create new "feuille" object, this function is called when a new month as began
        
        Args:
            api_key (APIKey): api_key
        """
        currentMonthDate = DateService.currentMonthDate()
        currentMonthTimestamp = DateService.dateToMonthTimestamp(currentMonthDate)

        print(f"{currentMonthTimestamp=}")
        if not Feuille.objects.filter(api_key=api_key, date=currentMonthTimestamp).first():
            default_factures_str : Factures = Factures.objects.filter(api_key=api_key).first()
            print(f"{default_factures_str=}")
            if default_factures_str:
                factures = default_factures_str.datas.replace("'", '"')
                Feuille(date=currentMonthTimestamp, factures=factures, api_key=api_key).save()
            
    @staticmethod
    def retrieve(api_key: APIKey, pk: int) -> Feuille:
        """Retrive feuille object with id=pk but all tdcs are ids not tdc objects 

        Args:
            api_key (APIKey): api_key
            pk (int): id as primary key

        Returns:
            Feuille: feuille object with out tdcs objects datas (ids instead)
        """
        feuille = Feuille.objects.filter(id=pk, api_key=api_key).first()
        
        if not feuille:
            return None
        
        feuille_timestamp__lte = feuille.date
        feuille_date_lte = datetime.datetime.fromtimestamp(feuille_timestamp__lte)
        feuille_next_date_lte = feuille_date_lte + relativedelta(months=1)
        
        tdcs = TicketDeCaisse.objects.filter(date__lte=feuille_next_date_lte, date__gte=feuille_date_lte, api_key=api_key)
        feuille.tickets = [tdc.id for tdc in tdcs]
        return feuille

    @staticmethod
    def retrieve_tdcs(api_key: APIKey, pk: int):
        """ retrieve all tdcs objects from feuille associed with pk variable

        Args:
            api_key (APIKey): api_key
            pk (int): id as primary key

        Returns:
            Django QuerySet: List of tdcs
        """
        feuille = Feuille.objects.get(api_key=api_key, id=pk)
        
        feuille_timestamp__lte = feuille.date
        feuille_date_lte = datetime.datetime.fromtimestamp(feuille_timestamp__lte)
        feuille_next_date_lte = feuille_date_lte + relativedelta(months=1)
        
        return TicketDeCaisse.objects.filter(api_key=api_key, date__lte=feuille_next_date_lte, date__gte=feuille_date_lte).all()

    @staticmethod
    def feuilleToDataTable(feuille : Feuille) -> TableFeuille:
        table_feuille : TableFeuille = TableFeuille.empty()
        factures = feuille.factures_json()
        
        if factures:
            for name, price in factures.items():
                table_feuille.add(category="Factures", name=name, price=price, date=None, required=True)
                
        if feuille.tickets:
            for ticketId in feuille.tickets:
                tdc = TicketDeCaisse.objects.filter(id=ticketId).first()
                if tdc:
                    table_feuille.add(
                        category=tdc.category.name, name=tdc.shop.name, price=tdc.total, date=tdc.date, required=tdc.category.required
                    )

        return table_feuille

    @staticmethod
    def feuilleSummary(f: Feuille, t: TableFeuille) -> Dict[str, float]:
        ttdepense_v = 0.0
        ttevitable_v = 0.0
        dateService = DateService()

        for _, c in t.items.items():
            c : TableFeuilleCategory = c
            ttdepense_v  += c.header.price
            ttevitable_v += c.header.priceOnlyRequired


        ffactures : TableFeuilleCategory = t.items.get('Factures')
        ttfactures = ffactures.header.price if ffactures else 0

        if f.tickets:
            tdcinf, tdcsup = f.tickets[0], f.tickets[-1]
            datebonreinf = TicketDeCaisse.objects.get(id=tdcinf).date
            datebornesup = TicketDeCaisse.objects.get(id=tdcsup).date
            datebonreinf = dateService.dateToDateObject(dateService.firstDayOfDate(dateService.DateToDateStr(datebonreinf)))
            datebornesup = dateService.DateToDateStr(datebornesup)

            currentDateSup = dateService.dateToDateObject(dateService.currentDateStr())
            lastDayDateSup = dateService.dateToDateObject(dateService.lastDatOfDate(datebornesup))
            lastSpendDate  = dateService.dateToDateObject(datebornesup)

            if lastSpendDate.month < currentDateSup.month or lastSpendDate.year < currentDateSup.year:
                datebornesup = lastDayDateSup
            elif lastSpendDate < currentDateSup:
                datebornesup = currentDateSup
            else:
                datebornesup = lastSpendDate

            datediff_days = max(0, (datebornesup - datebonreinf).days)+1
        else:
            datediff_days = 1

        decimalFormat = lambda d: float("{:.2f}".format(d))
        tttheorique_v = 1900

        return {
            "tttheorique_v": tttheorique_v,
            "ttdepense": decimalFormat(ttdepense_v),
            "factures": decimalFormat(ttfactures),
            "ttevitable": decimalFormat(ttevitable_v),
            "tteparge": decimalFormat(tttheorique_v - ttdepense_v),
            "ttconfort": decimalFormat(ttdepense_v - ttevitable_v),
            "dep": decimalFormat((ttdepense_v - ttfactures)),
            "mj": decimalFormat((ttdepense_v - ttfactures) / datediff_days)
        }