import logging

from django.core.management.base import BaseCommand
from django.utils import timezone
from sentry_sdk.crons import monitor

from imminent.models import Pdc
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Hazard Exposure Data"

    @monitor(monitor_slug=SentryMonitor.CHECK_PDC_STATUS)
    def handle(self, *args, **options):
        today_date = timezone.now().date()
        resp = Pdc.objects.filter(
            status=Pdc.Status.ACTIVE,
            end_date__lt=today_date,
        ).update(
            status=Pdc.Status.EXPIRED,
        )
        print(f"Updated: {resp}")
