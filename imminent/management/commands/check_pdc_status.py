import logging
import datetime

from django.core.management.base import BaseCommand

from imminent.models import Pdc


logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Import Hazard Exposure Data'

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        today_date = now.date()
        pdcs = Pdc.objects.filter(status=Pdc.Status.ACTIVE)
        for pdc in pdcs:
            if pdc.end_date and pdc.end_date < today_date:
                pdc.status = Pdc.Status.EXPIRED
                pdc.save(update_fields=['status'])
