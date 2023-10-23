from rest_framework import serializers
from .models import WeatherCache


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCache
        fields = '__all__'
