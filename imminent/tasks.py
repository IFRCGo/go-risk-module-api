import logging

from celery import shared_task
from django.core.management import call_command

from risk_module.cache import CacheKey, redis_lock
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


@shared_task
def create_pdc_data():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_DATA)) as acquired:
        if not acquired:
            logger.warning("CREATE_PDC_DATA is already running....")
            return
        call_command("create_pdc_data")


@shared_task
def create_pdc_daily():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_DAILY)) as acquired:
        if not acquired:
            logger.warning("CREATE_PDC_DAILY is already running.....")
            return
        call_command("create_pdc_daily")


@shared_task
def create_pdc_displacement():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_DISPLACEMENT)) as acquired:
        if not acquired:
            logger.warning("CREATE_PDC_DISPLACEMENT is already running.....")
            return
        call_command("create_pdc_displacement")


@shared_task
def create_pdc_polygon():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_POLYGON)) as acquired:
        if not acquired:
            logger.warning("CREATE_PDC_POLYGON is already running.....")
            return
        call_command("create_pdc_polygon")


@shared_task
def create_pdc_intensity():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_INTENSITY)) as acquired:
        if not acquired:
            logger.warning("CREATE_PDC_INTENSITY is already running.....")
            return
        call_command("create_pdc_intensity")


@shared_task
def check_pdc_status():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CHECK_PDC_STATUS)) as acquired:
        if not acquired:
            logger.warning("CHECK_PDC_STATUS is already running.....")
            return
        call_command("check_pdc_status")

@shared_task
def create_pdc_three_days_cou():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_THREE_DAYS_COU)) as acquired:
        if not acquired:
            logger.warning("CREATE_PDC_THREE_DAYS_COU is alreay running.....")
            return
        call_command("create_pdc_three_days_cou")

@shared_task
def create_pdc_five_days_cou():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_FIVE_DAYS_COU)) as acquired:
        if not acquired:
            logger.warning("CREATE_PDC_FIVE_DAYS_COU is already running......")
            return
        call_command("create_pdc_five_days_cou")

@shared_task
def import_earthquake_data():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.IMPORT_EARTHQUAKE_DATA)) as acquired:
        if not acquired:
            logger.warning("IMPORT_EARTHQUAKE_DATA is already running.....")
            return
        call_command("import_earthquake_data")


@shared_task
def create_adam_exposure():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_ADAM_EXPOSURE)) as acquired:
        if not acquired:
            logger.warning("CREATE_ADAM_EXPOSURE is already running.....")
            return
        call_command("create_adam_exposure")


@shared_task
def update_adam_cyclone():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.UPDATE_ADAM_CYCLONE)) as acquired:
        if not acquired:
            logger.warning("UPDATE_ADAM_CYCLONE is already running.....")
            return
        call_command("update_adam_cyclone")


@shared_task
def update_adam_alert_level():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.UPDATE_ADAM_ALERT_LEVEL)) as acquired:
        if not acquired:
            logger.warning("UPDATE_ADAM_ALERT_LEVEL is already running.....")
            return
        call_command("update_adam_alert_level")


@shared_task
def import_gdacs_data():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.IMPORT_GDACS_DATA)) as acquired:
        if not acquired:
            logger.warning("IMPORT_GDACS_DATA is already running.....")
            return
        call_command("import_gdacs_data")


@shared_task
def pull_meteoswiss():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.PULL_METEOSWISS)) as acquired:
        if not acquired:
            logger.warning("PULL_METEOSWISS is already running.....")
            return
        call_command("pull_meteoswiss")


@shared_task
def pull_meteoswiss_geo():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.PULL_METEOSWISS_GEO)) as acquired:
        if not acquired:
            logger.warning("PULL_METEOSWISS_GEO is already running.....")
            return
        call_command("pull_meteoswiss_geo")


@shared_task
def meteoswiss_agg():
    with redis_lock(CacheKey.get_sm_lock(SentryMonitor.METEOSWISS_AGG)) as acquired:
        if not acquired:
            logger.warning("METEOSWISS_AGG is already running.....")
            return
        call_command("meteoswiss_agg")


@shared_task
def check_not_provided_country():
    call_command("check_country_not_provided")
