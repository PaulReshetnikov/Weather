from django.db import models


class WeatherCache(models.Model):
    """Модель данных о погоде"""
    city = models.CharField(max_length=255, unique=True)
    temperature = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city


class CityModel(models.Model):
    """Модель данных координат города"""
    DoesNotExist = None
    city_name = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
