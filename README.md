# Сервис погоды
Эта инструкция поможет вам установить два моих проекта: проект на Django и чат-бота. Пожалуйста, следуйте этим шагам, чтобы успешно настроить окружение.


## Установка
### Создать виртуальное окружение
```shell
python -m venv venv
```

### Активировать окружение:
```shell
source\venv\bin\activate
```
### Склонировать репозиторий с GitLab
```shell
git clone https://github.com/PaulReshetnikov/Weather
```

### Установка зависимостей:
```shell
pip install -r requirements.txt
```

## Запуск проектов
### Для запуска проекта Django выполните:
```shell
python manage.py runserver
```
### Для запуска чат-бота:
```shell
python main.py
```
## Доступ проектов
-  Проект Django будет доступен по адресу http://localhost:8000/.
-  Чат-бот будет запущен и готов к использованию.

## API
- Для получения погоды по выбранной локации выполните запрос(на данный момент тестово работает на Калининграде, Москве и Набережных Челнах)
- /weather?city="city name" где "city name" - это название города на русском языке
```
/weather?city=<city name>
```
