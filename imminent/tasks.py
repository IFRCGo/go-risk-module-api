from celery import shared_task
from django.core.management import call_command
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from risk_module.cache import redis_lock, CacheKey


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_DATA))
@monitor(monitor_slug=SentryMonitor.CREATE_PDC_DATA)
def create_pdc_data():
    call_command(
        "create_pdc_data",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_DAILY))
@monitor(monitor_slug=SentryMonitor.CREATE_PDC_DAILY)
def create_pdc_daily():
    call_command(
        "create_pdc_daily",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_DISPLACEMENT))
@monitor(monitor_slug=SentryMonitor.CREATE_PDC_DISPLACEMENT)
def create_pdc_displacement():
    call_command(
        "create_pdc_displacement",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_POLYGON))
@monitor(monitor_slug=SentryMonitor.CREATE_PDC_POLYGON)
def create_pdc_polygon():
    call_command(
        "create_pdc_polygon",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_PDC_INTENSITY))
@monitor(monitor_slug=SentryMonitor.CREATE_PDC_INTENSITY)
def create_pdc_intensity():
    call_command(
        "create_pdc_intensity",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.CHECK_PDC_STATUS))
@monitor(monitor_slug=SentryMonitor.CHECK_PDC_STATUS)
def check_pdc_status():
    call_command(
        "check_pdc_status",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.IMPORT_EARTHQUAKE_DATA))
@monitor(monitor_slug=SentryMonitor.IMPORT_EARTHQUAKE_DATA)
def import_earthquake_data():
    call_command(
        "import_earthquake_data",
    )


@shared_task
def check_not_provided_country():
    call_command(
        "check_country_not_provided",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.CREATE_ADAM_EXPOSURE))
@monitor(monitor_slug=SentryMonitor.CREATE_ADAM_EXPOSURE)
def create_adam_exposure():
    call_command(
        "create_adam_exposure",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.UPDATE_ADAM_CYCLONE))
@monitor(monitor_slug=SentryMonitor.UPDATE_ADAM_CYCLONE)
def update_adam_cyclone():
    call_command(
        "update_adam_cyclone",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.UPDATE_ADAM_ALERT_LEVEL))
@monitor(monitor_slug=SentryMonitor.UPDATE_ADAM_ALERT_LEVEL)
def update_adam_alert_level():
    call_command(
        "update_adam_alert_level",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.IMPORT_GDACS_DATA))
@monitor(monitor_slug=SentryMonitor.IMPORT_GDACS_DATA)
def import_gdacs_data():
    call_command(
        "import_gdacs_data",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.PULL_METEOSWISS))
@monitor(monitor_slug=SentryMonitor.PULL_METEOSWISS)
def pull_meteoswiss():
    call_command(
        "pull_meteoswiss",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.PULL_METEOSWISS_GEO))
@monitor(monitor_slug=SentryMonitor.PULL_METEOSWISS_GEO)
def pull_meteoswiss_geo():
    call_command(
        "pull_meteoswiss_geo",
    )


@shared_task
@redis_lock(CacheKey.get_sm_lock(SentryMonitor.METEOSWISS_AGG))
@monitor(monitor_slug=SentryMonitor.METEOSWISS_AGG)
def meteoswiss_agg():
    call_command(
        "meteoswiss_agg",
    )
