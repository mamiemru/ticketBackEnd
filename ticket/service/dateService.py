
import time
import calendar

from datetime               import date
from datetime               import datetime
from dateutil.relativedelta import relativedelta

class DateService:

    @staticmethod
    def dateStrToDateYear(date : str) -> str:
        return datetime.strptime(date[6:10], "%Y").strftime("%d/%m/%Y 00:00:00")

    @staticmethod
    def dateStrToDayNumberOfTheYear(date : str) -> str:
        return datetime.strptime(date, "%d/%m/%Y %H:%M:%S").timetuple().tm_yday

    @staticmethod
    def dateStrAdd1Year(date : str) -> str:
        d : datetime = datetime.strptime(date, "%d/%m/%Y 00:00:00")
        return (d + relativedelta(years=1)).strftime("%d/%m/%Y 00:00:00")

    @staticmethod
    def dateSub1Month(date : str) -> str:
        d : datetime = datetime.strptime(date, "%d/%m/%Y 00:00:00")
        return (d - relativedelta(months=1)).strftime("%d/%m/%Y 00:00:00")

    @staticmethod
    def dateAdd1Month(date : str) -> str:
        d : datetime = datetime.strptime(date, "%d/%m/%Y 00:00:00")
        return (d + relativedelta(months=1)).strftime("%d/%m/%Y 00:00:00")

    @staticmethod
    def timestampToDate(timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")

    @staticmethod
    def currentDate():
        return date.today()

    @staticmethod
    def currentTimeStamp() -> int:
        return int(time.time())

    @staticmethod
    def currentDateStr():
        return date.today().strftime("%d/%m/%Y 00:00:00")

    @staticmethod
    def currentMonthDate():
        return date.today().strftime("01/%m/%Y 00:00:00")

    @staticmethod
    def yearmonthDate(yearmonth):
        return date(year=int(yearmonth[:4]), month=int(yearmonth[-2:]), day=1).strftime("01/%m/%Y 00:00:00")

    @staticmethod
    def firstDayOfDate(date="01/07/2022 09:00:00"):
        return DateService.dateToDateObject(date).strftime("01/%m/%Y 00:00:00")

    @staticmethod
    def currentEndMonthDateStr():
        currentDate = date.today()
        return date(currentDate.year, currentDate.month, calendar.monthrange(currentDate.year, currentDate.month)[1]).strftime("%d/%m/%Y 00:00:00")

    @staticmethod
    def lastDatOfDate(d="01/07/2022 09:00:00"):
        currentDate = DateService.dateToDateObject(d)
        return date(currentDate.year, currentDate.month, calendar.monthrange(currentDate.year, currentDate.month)[1]).strftime("%d/%m/%Y 00:00:00")


    @staticmethod
    def dateToMonthTimestamp(date="01/07/2022 09:00:00") -> float:
        return time.mktime(time.strptime(date[3:10], '%m/%Y'))

    @staticmethod
    def dateStrToTimestamp(date="01/07/2022 09:00:00") -> float:
        return time.mktime(time.strptime(date, "%d/%m/%Y %H:%M:%S"))

    @staticmethod
    def dateToDateObject(date="01/07/2022 09:00:00") -> datetime:
        return datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    
    @staticmethod
    def DateToDateStr(date : datetime, strft="%d/%m/%Y %H:%M:%S"):
        return date.strftime(strft)