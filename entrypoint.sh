#!/bin/sh
python manage.py makemigrations
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=admin12 python manage.py createsuperuser --username admin --email admin@email.com --noinput
exec "$@"