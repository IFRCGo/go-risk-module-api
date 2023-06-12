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


@shared_task
def create_adam_exposure():
    call_command('create_adam_exposure',)


@shared_task
def update_adam_cyclone():
    call_command('update_adam_cyclone',)


@shared_task
def update_adam_alert_level():
    call_command('update_adam_alert_level',)


@shared_task
def import_gdacs_data():
    call_command('import_gdacs_data',)


@shared_task
def pull_meteoswiss():
    call_command('pull_meteoswiss',)


@shared_task
def meteoswiss_agg():
    call_command('meteoroswiss_agg',)
