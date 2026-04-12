#!/bin/sh

set -e

export DJANGO_SETTINGS_MODULE=config.settings.prod

python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3