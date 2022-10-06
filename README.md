# Foodgram

![example workflow](https://github.com/nmutovkin/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Foodgram - сервис для любителей готовить! Создавайте рецепты, делитесь ими и пробуйте новые идеи.

# Локальный запуск проекта

Для локального запуска проекта необходимо установить Docker

Клонируем проект с github.

Создаем файл .env в папке infra. Заполняем переменные в соответствии с шаблоном .env.template.

Переходим в папку infra. Там выполняем команду docker-compose -d.

Для подготовки базы данных:

1) выполнить миграции docker-compose exec backend python manage.py migrate
2) собрать статику docker-compose exec backend python manage.py collectstatic --no-input
3) создать суперпользователя docker-compose exec backend python manage.py createsuperuser
4) если есть предварительный сгенерированный дамп базы данных, то можно наполнить ее используя docker-compose exec backend python manage.py loaddata dump.json

проект доступен по http://localhost
админ-зона http://localhost/admin
