#!/bin/bash -x

python manage.py collectstatic --noinput &
python manage.py migrate --noinput
celery -A risk_module worker --loglevel=info &
celery -A risk_module beat --max-interval 3600 -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler &
gunicorn risk_module.wsgi:application --bind 0.0.0.0:${SERVER_PORT}
