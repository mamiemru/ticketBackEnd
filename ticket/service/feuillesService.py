

import datetime
from dateutil.relativedelta import relativedelta

from typing import Dict

from ticket.models import Feuille
from ticket.models import TicketDeCaisse
from ticket.models import TicketDeCaisseTypeEnum

from ticket.service.dateService import DateService

from ticket.structs import TableFeuille

class FeuillesService():
    
    @staticmethod
    def retrieve(pk) -> Feuille:
        feuille = Feuille.objects.get(id=pk)
        
        feuille_timestamp__lte = feuille.date
        feuille_date_lte = datetime.datetime.fromtimestamp(feuille_timestamp__lte)
        feuille_next_date_lte = feuille_date_lte + relativedelta(months=1)
        
        tdcs = TicketDeCaisse.objects.filter(date__lte=feuille_next_date_lte, date__gte=feuille_date_lte)
        feuille.tickets = [tdc.id for tdc in tdcs]
        return feuille

    @staticmethod
    def retrieve_tdcs(pk):
        feuille = Feuille.objects.get(id=pk)
        
        feuille_timestamp__lte = feuille.date
        feuille_date_lte = datetime.datetime.fromtimestamp(feuille_timestamp__lte)
        feuille_next_date_lte = feuille_date_lte + relativedelta(months=1)
        
        return TicketDeCaisse.objects.filter(date__lte=feuille_next_date_lte, date__gte=feuille_date_lte).all()

    @staticmethod
    def feuilleToDataTable(feuille : Feuille) -> TableFeuille:
        l : TableFeuille = TableFeuille.empty()
        
        for name, price in feuille.factures_json().items():
            l.add(category="Factures", name=name, price=price, date=None, required=True)
            
        for ticketId in feuille.tickets:
            tdc = TicketDeCaisse.objects.filter(id=ticketId).first()
            if tdc:
                price = tdc.total()
                required = tdc.category.required
                l.add(category=tdc.category.name, name=tdc.shop.name, price=price, date=tdc.date, required=required)

        return l

    @staticmethod
    def feuilleSummary(f: Feuille, t: TableFeuille) -> Dict[str, float]:
        ttdepense_v = 0.0
        ttevitable_v = 0.0
        dateService = DateService()

        for k, c in t.items.items():
            c : TableFeuilleCategory = c
            ttdepense_v  += c.header.price
            ttevitable_v += c.header.priceOnlyRequired

        ffactures : TableFeuilleCategory = t.items['Factures']
        ttfactures = ffactures.header.price

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