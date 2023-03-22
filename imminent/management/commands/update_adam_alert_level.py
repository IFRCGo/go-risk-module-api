from django.core.management.base import BaseCommand

from common.models import HazardType
from imminent.models import Adam


class Command(BaseCommand):
    help = 'Update Adam Earthquake Alert Level'

    def handle(self, *args, **kwargs):
        adams = Adam.objects.filter(
            hazard_type=HazardType.EARTHQUAKE
        )
        for adam in adams:
            mag = adam.event_details.get('mag')
            if mag:
                if mag < 6.2:
                    alert_level = 'Green'
                elif mag > 6 and mag <= 6.5:
                    alert_level = 'Orange'
                elif mag > 6.5:
                    alert_level = 'Red'
            adam.event_details['alert_level'] = alert_level
            adam.save(update_fields=['event_details'])
