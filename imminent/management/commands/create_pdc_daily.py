import requests
import logging
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from imminent.models import Pdc
from common.models import HazardType


logger = logging.getLogger()


class Command(BaseCommand):
    help = "Import Active Hazards"

    def parse_timestamp(self, timestamp):
        # NOTE: all timestamp are in millisecond and with timezone `utc`
        return timezone.make_aware(datetime.datetime.utcfromtimestamp(int(timestamp) / 1000))

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_DAILY)
    def handle(self, *args, **options):
        # NOTE: Use the search hazard api for the information download
        # make sure to use filter the data
        url = "https://sentry.pdc.org/hp_srv/services/hazards/t/json/get_active_hazards"
        headers = {"Authorization": "Bearer {}".format(settings.PDC_ACCESS_TOKEN)}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            error_log = f"Error querying PDC data at {url}"
            logger.error(error_log)
            logger.error(response.content)
        response_data = response.json()
        for data in response_data:
            # NOTE: Filter the active hazard only
            # Update the hazard if it has expired
            hazard_type = data["type_ID"]
            hazard_status = data["status"]
            if hazard_status == "E":
                pdcs = Pdc.objects.filter(uuid=data["uuid"])
                for pdc in pdcs:
                    pdc.status = Pdc.Status.EXPIRED
                    pdc.save(update_fields=["status"])
            if hazard_status == "A":
                if hazard_type == "FLOOD":
                    hazard_type = HazardType.FLOOD
                    data = {
                        "hazard_id": data["hazard_ID"],
                        "hazard_name": data["hazard_Name"],
                        "latitude": data["latitude"],
                        "longitude": data["longitude"],
                        "description": data["description"],
                        "hazard_type": hazard_type,
                        "uuid": data["uuid"],
                        "start_date": self.parse_timestamp(data["start_Date"]),
                        "end_date": self.parse_timestamp(data["end_Date"]),
                        "status": Pdc.Status.ACTIVE,
                        "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                        "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                    }
                    Pdc.objects.get_or_create(**data)
                elif hazard_type == "CYCLONE":
                    hazard_type = HazardType.CYCLONE
                    data = {
                        "hazard_id": data["hazard_ID"],
                        "hazard_name": data["hazard_Name"],
                        "latitude": data["latitude"],
                        "longitude": data["longitude"],
                        "description": data["description"],
                        "hazard_type": hazard_type,
                        "uuid": data["uuid"],
                        "start_date": self.parse_timestamp(data["start_Date"]),
                        "end_date": self.parse_timestamp(data["end_Date"]),
                        "status": Pdc.Status.ACTIVE,
                        "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                        "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                    }
                    Pdc.objects.get_or_create(**data)
                elif hazard_type == "STORM":
                    hazard_type = HazardType.STORM
                    data = {
                        "hazard_id": data["hazard_ID"],
                        "hazard_name": data["hazard_Name"],
                        "latitude": data["latitude"],
                        "longitude": data["longitude"],
                        "description": data["description"],
                        "hazard_type": hazard_type,
                        "uuid": data["uuid"],
                        "start_date": self.parse_timestamp(data["start_Date"]),
                        "end_date": self.parse_timestamp(data["end_Date"]),
                        "status": Pdc.Status.ACTIVE,
                        "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                        "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                    }
                    Pdc.objects.get_or_create(**data)
                elif hazard_type == "DROUGHT":
                    hazard_type = HazardType.DROUGHT
                    data = {
                        "hazard_id": data["hazard_ID"],
                        "hazard_name": data["hazard_Name"],
                        "latitude": data["latitude"],
                        "longitude": data["longitude"],
                        "description": data["description"],
                        "hazard_type": hazard_type,
                        "uuid": data["uuid"],
                        "start_date": self.parse_timestamp(data["start_Date"]),
                        "end_date": self.parse_timestamp(data["end_Date"]),
                        "status": Pdc.Status.ACTIVE,
                        "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                        "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                    }
                    Pdc.objects.get_or_create(**data)
                elif hazard_type == "WIND":
                    hazard_type = HazardType.WIND
                    data = {
                        "hazard_id": data["hazard_ID"],
                        "hazard_name": data["hazard_Name"],
                        "latitude": data["latitude"],
                        "longitude": data["longitude"],
                        "description": data["description"],
                        "hazard_type": hazard_type,
                        "uuid": data["uuid"],
                        "start_date": self.parse_timestamp(data["start_Date"]),
                        "end_date": self.parse_timestamp(data["end_Date"]),
                        "status": Pdc.Status.ACTIVE,
                        "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                        "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                    }
                    Pdc.objects.get_or_create(**data)
                elif hazard_type == "TSUNAMI":
                    hazard_type = HazardType.TSUNAMI
                    data = {
                        "hazard_id": data["hazard_ID"],
                        "hazard_name": data["hazard_Name"],
                        "latitude": data["latitude"],
                        "longitude": data["longitude"],
                        "description": data["description"],
                        "hazard_type": hazard_type,
                        "uuid": data["uuid"],
                        "start_date": self.parse_timestamp(data["start_Date"]),
                        "end_date": self.parse_timestamp(data["end_Date"]),
                        "status": Pdc.Status.ACTIVE,
                        "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                        "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                    }
                    Pdc.objects.get_or_create(**data)
                elif hazard_type == "EARTHQUAKE":
                    hazard_type = HazardType.EARTHQUAKE
                    data = {
                        "hazard_id": data["hazard_ID"],
                        "hazard_name": data["hazard_Name"],
                        "latitude": data["latitude"],
                        "longitude": data["longitude"],
                        "description": data["description"],
                        "hazard_type": hazard_type,
                        "uuid": data["uuid"],
                        "start_date": self.parse_timestamp(data["start_Date"]),
                        "end_date": self.parse_timestamp(data["end_Date"]),
                        "status": Pdc.Status.ACTIVE,
                        "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                        "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                    }
                    Pdc.objects.get_or_create(**data)
                elif hazard_type == "WILDFIRE":
                    hazard_type = HazardType.WILDFIRE
                    pdc_updated_at = self.parse_timestamp(data["last_Update"])
                    if Pdc.objects.filter(
                        uuid=data["uuid"], hazard_type=hazard_type, pdc_updated_at=pdc_updated_at
                    ).exists():
                        continue
                    else:
                        data = {
                            "hazard_id": data["hazard_ID"],
                            "hazard_name": data["hazard_Name"],
                            "latitude": data["latitude"],
                            "longitude": data["longitude"],
                            "description": data["description"],
                            "hazard_type": hazard_type,
                            "uuid": data["uuid"],
                            "start_date": self.parse_timestamp(data["start_Date"]),
                            "end_date": self.parse_timestamp(data["end_Date"]),
                            "status": Pdc.Status.ACTIVE,
                            "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                            "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                        }
                        Pdc.objects.get_or_create(**data)
