from json import JSONEncoder
from django.urls import NoReverseMatch
from django.db.models import QuerySet
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumber
from decimal import *
class PhoneNumberEncoder(JSONEncoder):
    def default(self,o):
        if isinstance(o, PhoneNumber):
            return str(o)
        else:
            return super().default(o)
            
class DecimalEncoder(JSONEncoder):
    def default(self,o):
        if isinstance(o, Decimal):
            return int(o)
        else:
            return super().default(o)

class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            return super().default(o)


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, PhoneNumberEncoder, DecimalEncoder, JSONEncoder):
    encoders = {}

    def default(self, o):
        if isinstance(o, self.model):
            d = {}
            if hasattr(o, "get_api_url"):
                try:
                    d["href"] = o.get_api_url()
                except NoReverseMatch:
                    pass
            for property in self.properties:
                value = getattr(o, property)
                if property in self.encoders:
                    encoder = self.encoders[property]
                    value = encoder.default(value)
                d[property] = value
            d.update(self.get_extra_data(o))
            return d
        else:
            return super().default(o)

    def get_extra_data(self, o):
        return {}
