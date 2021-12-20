#!/bin/bash

python3 manage.py migrate --no-input

celery -A risk_module worker --loglevel=info &
celery -A risk_module beat --max-interval 3600 -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler &
python3 manage.py runserver 0.0.0.0:9001
