![YAMDB workflow](https://github.com/hydrospirt/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# yamdb_final (Открытый API YAMDB с workflow Docker)
---
## Описание

---

***YaMDB*** - это открытый API для отзывов, который позволяет пользователям ставить оценки и писать отзывы о произведениях искусства. Этот сервис предоставляет возможность получить доступ к множеству отзывов и оценок на различные категории произведений искусства, таких как фильмы, книги, музыка и многое другое.

---
### Технологии:
- Python 3.9
- Django 3.2
- djangorestframework 3.12.4
- ReDoc
- Docker 20.10.24
- Docker-compose
- Yandex.oblako

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:hydrospirt/yamdb_final.git
```

Cоздать и активировать виртуальное окружение:
Linux:
```
python3 -m venv env
source env/bin/activate
```
Windows:
```
py -3.9 -m venv env
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r api_yamdb/requirements.txt
```
Войдите на свой удаленный сервер.
Остановите службу nginx:
```
 sudo systemctl stop nginx
```
Установите docker:
```
sudo apt install docker.io
```
Установите docker-compose, с этим вам поможет ![официальная документация](https://docs.docker.com/compose/install/other/).

Локально отредактировать файл infra/nginx.conf, обязательно в строке server_name вписать IP-адрес сервера
Скопировать файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

Для работы с Workflow добавить в Secrets GitHub переменные окружения для работы:
```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь базы данных>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

SECRET_KEY=<секретный ключ проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
```
В workflow четыре задачи (job):

- проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final;
- сборка и доставка докер-образа для контейнера web на Docker Hub;
- автоматический деплой проекта на боевой сервер;
- отправка уведомления в Telegram о том, что процесс деплоя успешно завершился.

### После успешной сборки выполнить команды:

Создать миграции:
```
docker-compose exec web python manage.py makemigrations
```
Выполнить миграции:
```
docker-compose exec web python manage.py migrate
```
Создать супер пользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Подключить статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Автодобавление данных ../static/data/:
Название файлов: 'category.csv', 'genre.csv', 'titles.csv', 'users.csv', 'review.csv', 'comments.csv', 'genre_title.csv'
```
docker-compose exec web python3 manage.py fill_bd
```
Перейти по ссылке для проверки:
```
http://localhost/api/v1/
http://localhost/admin/
```
---
## Примеры запросов:
**Регистрация нового пользователя:**
Получить код подтверждения на переданный email. Права доступа: Доступно без токена. Использовать имя 'me' в качестве username запрещено. Поля email и username должны быть уникальными.
```sh
http://localhost:8000/api/v1/auth/signup/
```
**email** `required`: string <email> <= 254 characters
**username** `required`: string <= 150 characters ^ [\w.@+-]+\z
```sh
{
"email": "user@example.com",
"username": "string"
}
```

**Получение JWT-токена**
Получение JWT-токена в обмен на username и confirmation code. Права доступа: **Доступно без токена.**
```sh
http://localhost:8000/api/v1/auth/token/
```
**username** `required`: string <= 150 characters ^ [\w.@+-]+\z
**confirmation_code** `required`: string
```sh
{
"username": "string",
"confirmation_code": "string"
}
```
**Получение списка всех категорий**
Получить список всех категорий Права доступа: **Доступно без токена**
```sh
http://localhost:8000/api/v1/categories/
```
**search**:	string -> Поиск по названию категории
```sh
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
**Получение списка всех отзывов**
Получить список всех отзывов. Права доступа: **Доступно без токена.**
```sh
http://localhost:8000/api/v1/titles/{title_id}/reviews/
```
**title_id** `required`: integer -> ID произведения
```sh
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

---
# Автор
Эдуард Гумен - GitHub: https://github.com/hydrospirt
Андрей Тарасов - GitHub: https://github.com/babyshitt
Дмитрий Смолов - GitHub: https://github.com/DmitrySmolov