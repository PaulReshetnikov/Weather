from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WeatherCache, CityModel
from .serializers import WeatherSerializer
import requests
from datetime import datetime, timedelta,  timezone


class WeatherAPIView(APIView):
    YANDEX_API_KEY = 'YOUR_YANDEX_API'  # Замените на ваш собственный ключ
    """
    Получение данных о погоде для указанного города.
            Parameters:
                - request: Запрос, содержащий параметр 'city' с названием города.

            Returns:
                - JSON-ответ с данными о погоде для указанного города.

            Note:
                Данное представление ищет координаты для указанного города в базе данных, затем проверяет кеш данных о погоде.
                Если данных нет или они устарели, выполняется запрос к Yandex API для обновления данных.
    """

    def get(self, request):
        city = request.GET.get('city', '')
        # Поиск координат (широты и долготы) для указанного города в базе данных
        try:
            city_info = CityModel.objects.get(city_name=city)
            latitude = city_info.latitude
            longitude = city_info.longitude
        except CityModel.DoesNotExist:
            return Response({'error': 'Город не найден'}, status=404)

        weather_data = WeatherCache.objects.filter(city=city).first()

        # Если данных нет или они устарели, запрашиваем их у Yandex
        if not weather_data or (
                    datetime.now(timezone.utc) - weather_data.last_updated.replace(tzinfo=timezone.utc)
                ) > timedelta(minutes=30):
            # Формируем URL для запроса к Yandex API
            lang = 'ru_RU'

            url = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&lang={lang}'
            headers = {
                'X-Yandex-API-Key': self.YANDEX_API_KEY,
            }

            # Отправляем GET-запрос к Yandex API
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                yandex_data = response.json()
                temperature = yandex_data['fact']['temp']
                pressure = yandex_data['fact']['pressure_mm']
                wind_speed = yandex_data['fact']['wind_speed']

                # Обновляем или создаем запись в кеше
                if weather_data:
                    weather_data.temperature = temperature
                    weather_data.pressure = pressure
                    weather_data.wind_speed = wind_speed
                else:
                    weather_data = WeatherCache(city=city,
                                                temperature=temperature,
                                                pressure=pressure,
                                                wind_speed=wind_speed
                                                )
                weather_data.save()
            else:
                return Response({'error': 'Ошибка при получении данных о погоде'}, status=response.status_code)

        serializer = WeatherSerializer(weather_data)
        return Response(serializer.data)
