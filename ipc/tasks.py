from celery import shared_task
from django.core.management import call_command


@shared_task
def import_think_hazard_informations():
    call_command('create_hazard_information',)
