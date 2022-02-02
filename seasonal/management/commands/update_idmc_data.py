from django.core.management.base import BaseCommand

from seasonal.models import Idmc
from common.models import HazardType


class Command(BaseCommand):
    help = 'Import Ipc Data'

    def handle(self, *args, **options):
        idmcs = Idmc.objects.filter(hazard_type=HazardType.STORM)
        for idmc in idmcs:
            idmc.hazard_type = HazardType.CYCLONE
            idmc.save(update_fields=['hazard_type'])
