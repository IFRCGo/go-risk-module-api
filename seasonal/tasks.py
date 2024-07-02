from celery import shared_task
from django.core.management import call_command
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from risk_module.cache import redis_lock, CacheKey


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_HAZARD_INFORMATION))
@monitor(monitor_slug=SentryMonitor.CREATE_HAZARD_INFORMATION)
def import_think_hazard_informations():
    call_command(
        "create_hazard_information",
    )
