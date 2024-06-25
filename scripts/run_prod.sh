#!/bin/bash -x

python manage.py collectstatic --noinput &
python manage.py migrate --noinput

gunicorn risk_module.wsgi:application --bind 0.0.0.0:9007
