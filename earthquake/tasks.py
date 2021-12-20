from celery import shared_task
from django.core.management import call_command


@shared_task
def import_earthquake_data():
    call_command('import_earthquake_data',)
