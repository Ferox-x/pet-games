[![Test coverage][coveralls-image]][coveralls-url]

## Brain Development Games 
#### Пользовательская платформа с мини-играми для развития интеллектуальных способностей.

[Техническое задание на разработку](./docs/technical_requirements.md)

____

## Как запустить проект:

1) Клонировать репозиторий и перейти в него в командной строке:

`git clone git@github.com:Ferox-x/pet-games.git`

2) Cоздать и активировать виртуальное окружение:

`python -m venv venv`

`source venv/Scripts/activate`

3) Установить зависимости из файла requirements.txt:

`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

4) Выполнить миграции:

`python manage.py makemigrations`

`python manage.py migrate`

5) Заполнить базу данных, с помощью management комманд:

`python manage.py makefixtures`

`python manage.py loaddata fixtures/*.json`

6) Создать суперпользователя, с помощью комманды:

`python manage.py createsuperuser`

7) Запустить сервер:

`python manage.py runserver`

## Эндпоинты для взаимодействия с ресурсами:
```bash
  - /api/v1/stroop/ (GET): Таблица лидеров игры Струпа.
  - /api/v1/schulte/ (GET): Таблица лидеров игры Шульте.
```
### Примеры запросов
| Тип запроса | Эндпоинт               | Исходящие данные | Ответ                                                                                                                                  |
|-------------|------------------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| GET         | ```/api/v1/stroop/```  | *_________*      | [{ <br/> "username": User44, <br/> "record": "87 - 50 - 137", <br/> "score": 9898, <br/> "date": "2022-08-05T05:18:40.794000Z" <br/>}] |
| GET         | ```/api/v1/schulte/``` | *_________*      | [{ <br/> "username": User81, <br/> "record": "1226", <br/> "date": "2022-08-05T09:54:36.708000Z", <br/>}]   

## **Разработчики группового проекта:**

Frontend and Backend:
- Егор Малов: https://github.com/Ferox-x
- Александр Кондратьев: https://github.com/anywindblows

Дизайн:
- Юлия Конохова: https://github.com/cantchoosecolor
