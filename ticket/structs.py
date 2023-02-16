

#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import dataclasses

from typing import List
from typing import Dict
from dataclasses import dataclass

@dataclass
class TableFeuilleRow:
    name : str
    date : str
    price : float
    priceOnlyRequired : float

    def __init__(self, name, price, date, required:bool=False):
        self.name  = name
        self.price = price
        self.date  = date
        self.priceOnlyRequired = price if required else 0.0

    @staticmethod
    def empty(name=None):
        return TableFeuilleRow(name, 0.0, None, False)

    def to_json(self):
        return {
            "name": self.name,
            "date": self.date,
            "price": self.price,
            "priceOnlyRequired": self.priceOnlyRequired
        }

@dataclass
class TableFeuilleBody:
    name: str
    header: TableFeuilleRow
    rows: List[TableFeuilleRow]

    def __init__(self, name):
        self.name = name
        self.header = TableFeuilleRow.empty(name=None)
        self.header.name = name
        self.rows = list()

    def add(self, name, price, date, required=False):
        self.rows.append(TableFeuilleRow(name=name, price=price, date=date, required=required))
        self.header.price += price
        if required:
            self.header.priceOnlyRequired += price

    def isSingleton(self) -> bool:
        return len(self.rows) == 1

    def getSingleton(self) -> TableFeuilleRow:
        return self.rows[0]

    @staticmethod
    def empty(id=None):
        return TableFeuilleBody(id=id, header=TableFeuilleRow.empty(), rows=list())

    def to_json(self):
        return {
            "name": self.name,
            "header": self.header.to_json(),
            "rows": [x.to_json() for x in self.rows]
        }

@dataclass
class TableFeuilleCategory:
    category: str
    header: TableFeuilleRow
    body: Dict[str, TableFeuilleBody]

    def add(self, category, name, price, date, required):
        if not name in self.body:
            self.body[name] = TableFeuilleBody(name=name)
        self.body[name].add(name, price, date=date, required=required)
        self.header.price += price
        if required:
            self.header.priceOnlyRequired += price

    def isSingleton(self) -> bool:
        k = self.body.keys()
        if len(k) == 1:
            kk = list(k)[0]
            return self.body[kk].isSingleton()
        return False

    def getSingleton(self) -> TableFeuilleBody:
        return self.body[list(self.body.keys())[0]]

    @staticmethod
    def empty(category=None):
        return TableFeuilleCategory(category=category, header=TableFeuilleRow.empty(), body=dict())

    def to_json(self):
        return {
            "category": self.category,
            "header": self.header.to_json(),
            "body": {
                x:y.to_json() for x,y in self.body.items()
            }
        }

@dataclass
class TableFeuille:
    items: Dict[str, TableFeuilleCategory]
    
    def add(self, category, name, price, date, required):
        if not category in self.items:
            self.items[category] = TableFeuilleCategory.empty(category=category)
        self.items[category].add(category=category, name=name, price=price, date=date, required=required)

    @staticmethod
    def empty():
        return TableFeuille(items=dict())

    def to_json(self):
        return {x:y.to_json() for x,y in self.items.items()}
    
    
@dataclass
class ApexChartSerie:
    name: str
    type: str
    data: List[any]

class ApexChart:
    
    @staticmethod
    def to_type_column(x, series: List[ApexChartSerie], title_text):
        return {
            'series': map(dataclasses.asdict, series),
            'chartOptions': {
                'chart': { 'height': 300, 'type': 'line', 'zoom': { 'enabled': False } },
                'dataLabels': { 'enabled': False },
                'stroke': { 'curve': 'straight' },
                'title': { 'text': title_text, 'align': 'left' },
                'grid': { 'row': { 'colors': ['#f3f3f3', 'transparent'],  'opacity': 0.5 },},
                'xaxis': { 'categories': x, 'title': { 'text': '' } }
            }
        }