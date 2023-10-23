import telebot
import requests
from telebot import types
import config

TOKEN = config.TOKEN_BOT
WEATHER_API_KEY = config.API_KEY

# Инициализация бота с использованием токена
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик  команды '/start'.
    Приветствует пользователя и предоставляет кнопку для запроса погоды.
    """
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Узнать погоду", callback_data="get_weather")
    markup.add(button)
    bot.reply_to(message, "Нажмите на кнопку 'Узнать погоду', чтобы получить информацию о погоде в вашем городе.",
                 reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "get_weather")
def request_city(call):
    """ Обработчик для запроса погоды. Отправляет запрос пользователю на ввод названия города."""
    bot.send_message(call.message.chat.id, "Введите название города:")


@bot.message_handler(func=lambda message: True)
def get_weather(message):
    """ Обработчик для получения данных о погоде и отправки ответа пользователю."""
    city = message.text
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(weather_url)
    data = response.json()
    if response.status_code == 200:
        temperature = data['main']['temp']
        response_text = f'Погода в {city}: {temperature}°C'
    else:
        response_text = 'Не удалось получить данные о погоде. Проверьте название города.'
    bot.reply_to(message, response_text)


# Запуск бота и ожидание новых сообщений
bot.polling()
