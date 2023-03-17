from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name="citylocation", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Data(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    value = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    city = models.ForeignKey(City, related_name="data", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class CityGeojson(models.Model):
    @property
    def pk(self):
        return self.id  # your pk
    geojson = models.JSONField()
    
    def __str__(self):
        return self.__str__()
    
class CountryGeojson(models.Model):
    geojson = models.JSONField()
    
    def __str__(self):
        return self.__str__()
