from celery import shared_task
from django.core.management import call_command


@shared_task
def create_pdc_data():
    call_command('create_pdc_data',)


@shared_task
def create_pdc_displacement():
    call_command('create_pdc_displacement',)


@shared_task
def create_pdc_polygon():
    call_command('create_pdc_polygon',)
