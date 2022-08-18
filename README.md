## Brain Development Games 
#### Пользовательская платформа с мини-играми для развития интеллектуальных способностей.

[Техническое задание на разработку](./docs/technical_requirements.md)

____

# Как запустить проект:

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

## **Разработчики группового проекта:**

- Егор Малов: https://github.com/Ferox-x
- Александр Кондратьев: https://github.com/anywindblows
