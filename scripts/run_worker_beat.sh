#!/bin/bash -x

celery -A risk_module beat --max-interval 3600 -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
