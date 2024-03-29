# 1. Цель проекта

Цель проекта — разработать платформу, включающую в себя мини-игры
(далее приложения), направленные на развитие интеллектуальных способностей.
Пользователь платформы может пользоваться мини-играми, настраивать их параметры,
а так же соревноваться с другими пользователями платформы, путем продвижения по
таблице лидеров.


# 2. Описание системы

Система состоит из следующих основных функциональных блоков:

1. Регистрация, аутентификация и авторизация.
2. Приложения.
3. Таблица результатов пользователей (leaderboards).
4. Личный кабинет пользователя.
5. Служба поддержки пользователей.
6. Leaderboard API


## 2.1. Типы пользователей

Система предусматривает следующие типы пользователей системы:

1. Гость.
2. Авторизированный пользоавтель.
3. Администратор.
4. Модератор (Служба поддержки пользователей).

## 2.2. Регистрация

Регистрация пользователя подразумевает заполнение формы со следующими полями:

* nickname - обязательное поле
* email — обязательное поле
* Имя и фамилия — обязательное поле
* пароль — обязательное поле
* страна - необязательное поле


## 2.3. Аутентификация пользователя

Аутентификация пользователя осуществляется по nickname и паролю.


## 2.4. Функционал для пользователя

Пользователь после аутентификации (ввода логина и пароля) получает доступ к 
своему пользовательскому функционалу в Системе. Этот функционал состоит из
следующих блоков:

1. Редактирование данных профиля
2. Использования мини-игр размещенных на платформе
3. Отслеживание рейтинга
4. Связь с службой поддержки, путем создания обращения (ticket`a).

### 2.4.1. Редактирование профиля

В этом разделе у автора есть возможность редактирования данных
своего профиля — nickname, описание, имя и фамилия, email, страна, изображение пользователя.

Должна быть возможность сменить пароль, подтвердив свой старый пароль.

Если дизайн Системы будет подразумевать какие-то изображения для кастомизации
страницы Системы, то эти изображения тоже должны редактироваться из профиля
автора.

## 2.5. Функционал для гостя

1. Гость может использовать приложения размещенные на площадке Системы.

# 3. Игры

### 3.1 Игра Шульте

Таблица Шульте – квадратная матрица, в ячейках которой в произвольном порядке
размещены числа.

#### 3.1. Функционал Шульте

Функционал: 
 - Результаты
 - Restart game

#### 3.1.2 Рейтинг Шульте

Модель: 
 - User (Пользователь)
 - Datetime (Время рекорда)
 - Time (Рекорд)

### 3.2 Игра Струпа

Тест Струпа способствует развитию связи между чтением слов и их восприятием, 
а также повышает концентрацию внимания и его переключаемость. 
Смена обычного алгоритма- сначала читать, а потом воспринимать - на аналогичный, 
но обратный- сначала воспринимать, а потом читать - заставляет мозг выполнять
двойную работу.
        

#### 3.2.1 Функционал Струпа

Функционал: 
 - Результаты
 - Выбор времени игры
 - Счёт

#### 3.2.2 Рейтинг Струпа

Модель:
 - User (Пользователь)
 - Datetime (Время рекорда)
 - Record (Рекорд)
 - Score (Счёт)

# 4. Предлагаемый стек технологий
Для реализации системы предлагается следующий стек технологий:

* Бэкенд:
    - Язык Python
    - Фреймворк Django
    - Django REST framework
    - PostgreSQL
* Фронтенд:
    - JavaScript
* Дизайн:
    - Figma
* Деплой:
    - Docker
    - Nginx
    - Gunicorn

# 5. Требования к дизайну

Минимализм, лаконичность, акцент на контент. Белый фон. Должен присутствовать
логотип Системы на странице. Логотип надо разработать в рамках
этого проекта.
