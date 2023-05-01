![YAMDB workflow](https://github.com/hydrospirt/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# yamdb_final
## Описание
***YaMDB*** - это открытый API для отзывов, который позволяет пользователям ставить оценки и писать отзывы о произведениях искусства. Этот сервис предоставляет возможность получить доступ к множеству отзывов и оценок на различные категории произведений искусства, таких как фильмы, книги, музыка и многое другое.

С помощью ***YaMDB*** пользователи могут ставить оценки произведениям искусства, выражая свое мнение о них. Кроме того, они могут писать отзывы, в которых описывают свои впечатления от произведения. Это позволяет пользователям делиться своими мыслями и чувствами с другими людьми, а также получать информацию от других пользователей, которые уже оценили произведение.

> ***YaMDB*** предоставляет возможность получить доступ к надежной и актуальной информации об отзывах и оценках на произведениях искусства. Это позволяет пользователям принимать более обоснованные решения при выборе произведения для просмотра или прочтения. Кроме того, сервис помогает пользователям оценить качество произведения и сравнить его с другими произведениями в той же категории.

***YaMDB*** является открытым API, что означает, что любой разработчик может использовать его для создания своего собственного приложения. Это дает возможность создавать новые приложения, которые будут использовать информацию, предоставляемую сервисом, для различных целей. Например, можно создать приложение, которое будет предоставлять пользователю рекомендации на основе его предпочтений и оценок.

> В целом, ***YaMDB*** - это полезный сервис для всех, кто интересуется произведениями искусства. Он предоставляет возможность получить доступ к множеству отзывов и оценок на различные категории произведений искусства, а также позволяет пользователям делиться своими мыслями и чувствами с другими людьми. Кроме того, это открытый API, который может быть использован для создания различных приложений, основанных на информации, предоставляемой сервисом.
### Технологии:
- Python 3.9
- Django 3.2
- djangorestframework 3.12.4
- ReDoc
- Docker 20.10.24
- Docker-compose
- Yandex.oblako

### Как запустить проект и упаковать в Docker-compose:

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
python3 -m pip install --upgrade pip
pip install -r api_yamdb/requirements.txt
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

Создаем Docker-compose:
```
docker-compose up -d --build
```

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

