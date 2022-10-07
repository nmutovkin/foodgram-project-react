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
* Создаем суперпользователя ```docker-compose exec backend python manage.py createsuperuser```\

Если есть предварительно сгенерированный дамп базы данных, наполните ее командой
```docker-compose exec backend python manage.py loaddata dump.json```

После этого проект будет доступен по ```http://localhost```
Админ-зона проекта ```http://localhost/admin```
