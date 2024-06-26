from celery import shared_task
from django.core.management import call_command
from risk_module.sentry import SentryMonitor
from sentry_sdk.crons import monitor


@shared_task
@monitor(monitor_slug=SentryMonitor.CREATE_HAZARD_INFORMATION)
def import_think_hazard_informations():
    call_command(
        "create_hazard_information",
    )
