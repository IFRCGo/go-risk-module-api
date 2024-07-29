import logging

from celery import shared_task
from django.core.management import call_command

from risk_module.cache import CacheKey, redis_lock
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


@shared_task
def import_think_hazard_informations():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_HAZARD_INFORMATION)) as acquired:
        if not acquired:
            logger.warning("CREATE_HAZARD_INFORMATION is already running....")
            return
        call_command("create_hazard_information")
