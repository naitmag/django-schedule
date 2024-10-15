# Учебная Веб-Платформа для Расписания

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

Веб-платформа, разработанная на базе **Django** и **JavaScript**, предназначена для использования в учебных заведениях. Платформа предоставляет функционал для управления расписанием занятий, профилями студентов и преподавателей, а также поддерживает авторизацию пользователей. Система рассчитана на работу с высокими нагрузками и ориентирована на удобный пользовательский интерфейс. Проект выполнен в рамках дипломной работы.

## Особенности

- **Авторизация и аутентификация**: система поддерживает регистрацию и авторизацию студентов и преподавателей.
- **Профили пользователей**: студенты и преподаватели могут управлять своими профилями.
- **Расписание лекций по неделям**: отображение расписания с гибкой навигацией по неделям и поддержкой фильтрации по преподавателю или группе.
- **Поддержка импорта данных**: суперпользователи могут добавлять расписание через загрузку Excel файлов.
- **Масштабируемость**: проект спроектирован для работы с большими объемами данных и поддерживает высокие нагрузки.

## Стек технологий

- **Backend**: Python, Django
- **Frontend**: JavaScript, HTML, CSS
- **База данных**: PostgreSQL
- **Кэширование**: Redis
- **Инфраструктура**: Docker, Nginx, VPS
- **Прочее**: Архитектурное проектирование

## Скриншоты

### Главная страница

![Главная страница](https://i.imgur.com/9j6hdlr.png)

### Страница расписания

![Страница расписания](https://i.imgur.com/FkpkVP0.png)


## Установка

### Требования

- Python 3.12
- Django 5.1.1
- PostgreSQL
- Redis

### Шаги по установке

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/naitmag/django-schedule
    ```

2. Перейдите в директорию проекта:

    ```bash
    cd django-schedule
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Настройте переменные окружения:

    В файле `.env`:

    ```bash
    DOMAIN_NAME=your-domain.com
    DEBUG=False
    SECRET_KEY=your-secret-key
    ```

5. Настройте базу данных в `settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

6. Примените миграции:

    ```bash
    python manage.py migrate
    ```

7. Создайте суперпользователя:

    ```bash
    python manage.py createsuperuser
    ```

8. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

9. (Необязательно) Запустите Redis и другие службы с помощью Docker Compose:

    ```bash
    docker-compose up
    ```

## Использование

1. Войдите в систему через созданного суперпользователя.
2. Управляйте профилем студента или преподавателя.
3. Добавляйте или просматривайте расписание занятий.
4. Суперпользователи могут загружать расписания через Excel файлы.

## Контакты

Если у вас есть вопросы или предложения, свяжитесь с разработчиком через [LinkedIn](https://www.linkedin.com/in/yarm-dev/).
