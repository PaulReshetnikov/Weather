from django.contrib import admin
from .models import *


class CityAdmin(admin.ModelAdmin):
    pass


class WeatherAdmin(admin.ModelAdmin):
    pass


admin.site.register(CityModel, CityAdmin)
admin.site.register(WeatherCache, WeatherAdmin)
