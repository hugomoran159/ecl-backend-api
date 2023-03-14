import json
from eclData.models import CityGeojson as CountryGeojson
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    cityGeojson = json.loads("static/citydata.geojson")
    CityGeojson.objects.create(geojson=cityGeojson)
                
                
    countryGeojson = json.loads("static/country-mod.geojson")
    CountryGeojson.objects.create(geojson=countryGeojson)
        
        