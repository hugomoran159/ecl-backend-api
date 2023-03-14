import json
from eclData.models import CityGeojson, CountryGeojson
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    with open("static/citydata.geojson") as f:
        cityGeojson = json.loads(f.read())
    CityGeojson.objects.create(geojson=cityGeojson)
                
    with open("static/country-mod.geojson") as f:
        countryGeojson = json.loads(f.read())
    CountryGeojson.objects.create(geojson=countryGeojson)
        
        