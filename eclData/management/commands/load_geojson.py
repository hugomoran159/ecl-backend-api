import json
from eclData.models import CityGeojson, CountryGeojson
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "updates city data"
    
    def handle(self, *args, **options):
        
        CityGeojson.objects.all().delete()
        CountryGeojson.objects.all().delete()
        
        with open("static/citydata.geojson") as f:
            cityGeojson = json.loads(f.read())
        cityGeojsonString = json.dumps(cityGeojson, indent=None)
        CityGeojson.objects.create(geojson=(cityGeojsonString))
                    
        with open("static/countries-mod.geojson") as f:
            countryGeojson = json.loads(f.read())
        countryGeojsonString = json.dumps(countryGeojson, indent=None)
        CountryGeojson.objects.create(geojson=(countryGeojsonString))
    
        self.stdout.write("", ending="Data successfully updated")
        
        