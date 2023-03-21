import graphene
from graphene_django import DjangoObjectType
from eclData.models import City as CityModel
from eclData.models import Data as DataModel
from eclData.models import Country as CountryModel
from eclData.models import CityGeojson as CityGeojsonModel
from eclData.models import CountryGeojson as CountryGeojsonModel
from graphene import Node






class Country(DjangoObjectType):
    class Meta:
        model = CountryModel



class Data(DjangoObjectType):
    class Meta:
        model = DataModel


class City(DjangoObjectType):
    class Meta:
        model = CityModel

        
class CityGeojson(DjangoObjectType):
    class Meta:
        model = CityGeojsonModel

class CountryGeojson(DjangoObjectType):
    class Meta:
        model = CountryGeojsonModel


class Query(graphene.ObjectType):
    cities = graphene.List(City)
    data = graphene.List(Data)
    country = graphene.List(Country)
    country_geojson = graphene.List(CountryGeojson)
    city_geojson = graphene.List(CityGeojson)

    def resolve_cities(self, info):
        return CityModel.objects.all()

    def resolve_data(self, info):
        return DataModel.objects.all()

    def resolve_country(self, info):
        return CountryModel.objects.all()
    
    def resolve_country_geojson(self, info):
        return CountryGeojsonModel.objects.all()

    def resolve_city_geojson(self, info):
        return CityGeojsonModel.objects.all()


schema = graphene.Schema(query=Query)
