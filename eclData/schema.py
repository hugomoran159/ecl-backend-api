import graphene
from graphene_django import DjangoObjectType
from eclData.models import City as CityModel
from eclData.models import Data as DataModel
from eclData.models import Country as CountryModel
from graphene import Node


class Connection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info):
        return self.length


class Country(DjangoObjectType):
    class Meta:
        model = CountryModel
        interfaces = (Node,)
        filter_fields = ("name",)
        connection_class = Connection


class Data(DjangoObjectType):
    class Meta:
        model = DataModel
        interfaces = (Node,)
        filter_fields = ("name",)
        connection_class = Connection


class City(DjangoObjectType):
    class Meta:
        model = CityModel
        interfaces = (Node,)
        filter_fields = ("name",)
        connection_class = Connection

    """

    
    @classmethod
    def get_node(cls, info, id):
        return City.objects.get(id=id)
    """


class Query(graphene.ObjectType):
    city_by_name = graphene.Field(City, name=graphene.String(required=True))
    cities = graphene.List(City)
    data = graphene.List(Data)
    data_by_name = graphene.Field(Data, name=graphene.String(required=True))
    country = graphene.List(Country)
    country_by_name = graphene.Field(Country, name=graphene.String(required=True))

    def resolve_cities(self, info):
        return CityModel.objects.all()

    def resolve_data(self, info):
        return DataModel.objects.all()

    def resolve_city_by_name(self, info, name):
        return CityModel.objects.get(name=name)

    def resolve_data_by_name(self, info, name):
        return DataModel.objects.filter(city=self, name=name)

    def resolve_country(self, info):
        return CountryModel.objects.all()

    def resolve_country_by_name(self, info, name):
        return CountryModel.objects.get(name=name)


schema = graphene.Schema(query=Query)
