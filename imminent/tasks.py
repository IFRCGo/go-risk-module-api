from celery import shared_task
from django.core.management import call_command


@shared_task
def create_pdc_data():
    call_command('create_pdc_data',)


@shared_task
def create_pdc_daily():
    call_command('create_pdc_daily',)


@shared_task
def create_pdc_displacement():
    call_command('create_pdc_displacement',)


@shared_task
def create_pdc_polygon():
    call_command('create_pdc_polygon',)


@shared_task
def create_pdc_intensity():
    call_command('create_pdc_intensity',)


@shared_task
def check_pdc_status():
    call_command('check_pdc_status',)


@shared_task
def import_earthquake_data():
    call_command('import_earthquake_data',)


@shared_task
def check_not_provided_country():
    call_command('check_country_not_provided',)
