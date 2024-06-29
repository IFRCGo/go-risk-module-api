import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from imminent.models import Pdc


logger = logging.getLogger()


class Command(BaseCommand):
    help = "Import Hazard Exposure Data"

    def handle(self, *args, **options):
        today_date = timezone.now().date()
        resp = (
            Pdc.objects.filter(
                status=Pdc.Status.ACTIVE,
                end_date__lt=today_date,
            ).update(
                status=Pdc.Status.EXPIRED,
            )
        )
        print(f'Updated: {resp}')
