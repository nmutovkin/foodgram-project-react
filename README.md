# Foodgram

![example workflow](https://github.com/nmutovkin/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Foodgram - сервис для любителей готовить! Создавайте рецепты, делитесь ими и пробуйте новые идеи. Сервис позволяет публиковать рецепты, комментировать их, добавлять рецепты в список покупок, составлять список избранных рецептов.

# Технологии

* Python
* Django
* Django REST Framework
* Docker / Docker-compose

# Локальный деплой сервиса

Для локального запуска проекта необходимо установить Docker

Клонируем проект с github.

```git clone https://github.com/nmutovkin/foodgram-project-react.git```

Создаем файл .env в папке infra.

```touch infra/.env```

Заполняем переменные окружения в соответствии с шаблоном .env.template.

Далее, выполняем следующие команды

```
cd infra
docker-compose -d.
```

Для подготовки базы данных:

* Выполняем миграции ```docker-compose exec backend python manage.py migrate```
* Собираем статику ```docker-compose exec backend python manage.py collectstatic --no-input```
* Создаем суперпользователя ```docker-compose exec backend python manage.py createsuperuser```

Если есть предварительно сгенерированный дамп базы данных, наполните ее командой
```docker-compose exec backend python manage.py loaddata dump.json```

После этого проект будет доступен по ```http://localhost```
Админ-зона проекта ```http://localhost/admin```

# Авторизация

## Создание пользователя
**POST /api/users/**

**REQUEST**
```
{
  "email": "iivanov@yandex.ru",
  "username": "ivan.ivanov",
  "first_name": "Иван",
  "last_name": "Иванов",
  "password": "qwerty"
}
```

## Получение токена
**POST /api/auth/token/login/**

**REQUEST**
```
{
  "password": "string",
  "email": "string"
}
```

**RESPONSE**
```
{
    auth_token": "string"
}
```

# Примеры запросов к API

## Получение списка рецептов

**GET /api/recipes/**

**RESPONSE**
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "_gj3sla4lfAApF5stiCjPjTTdmfJagFoqXPBZdfWF1eghW2U7oNyy@El5tVMfH76y6gz",
        "first_name": "Иван",
        "last_name": "Иванов",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

## Публикация нового рецепта

**POST /api/recipes/**

**REQUEST**
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

**RESPONSE**
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "Cg8FndYc3B7m4t96SXNyXbd+MaGD6jivm292eAFMw5BIfiRRJ.boAFbQagt48+TCBQ-Eicdxa-v1kMfNELNa9eQqX6HgOw.GfZisz",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

# Автор
Никита Мутовкин
