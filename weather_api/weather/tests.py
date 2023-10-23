from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import *


class WeatherAPIViewTestCase(TestCase):
    def setUp(self):
        # Выполняется перед каждым тестом
        self.client = APIClient()

    def test_weather_data_retrieval(self):
        # Создаем объект CityModel для тестирования
        city = 'Абакан'
        CityModel.objects.create(city_name=city, latitude=53.72, longitude=91.43)

        # Создаем объект WeatherCache для тестирования
        WeatherCache.objects.create(city=city, temperature=10, pressure=750, wind_speed=5.0)

        # Формируем URL для тестирования
        url = reverse('weather-api')

        # Выполняем GET-запрос к вашему представлению
        response = self.client.get(url, {'city': city})

        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в ответе есть ожидаемые данные
        self.assertIn('temperature', response.data)
        self.assertIn('pressure', response.data)
        self.assertIn('wind_speed', response.data)

    def test_weather_data_invalid_city(self):
        # Формируем URL для тестирования с неверным городом
        url = reverse('weather-api')

        # Выполняем GET-запрос с неверным городом
        response = self.client.get(url, {'city': 'NonExistentCity'})

        # Проверяем, что запрос завершился с ошибкой (код 404)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
