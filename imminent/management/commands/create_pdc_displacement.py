import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.models import Country
from common.utils import logging_response_context
from imminent.models import Pdc, PdcDisplacement
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Hazard Exposure Data"

    @staticmethod
    def fetch_pdc_data(uuid):
        url = f"https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/latest/"
        headers = {"Authorization": f"Bearer {settings.PDC_ACCESS_TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logger.error(
                "Error querying PDC Exposure data",
                extra=logging_response_context(response),
            )
            return None

        return response.json()

    @staticmethod
    def create_pdc_displacement(pdc, hazard_type, data):
        pdc_displacement_list = []

        for d in data:
            iso3 = d["country"].lower()
            country = Country.objects.filter(iso3=iso3).first()

            if country:
                c_data = {
                    "country": country,
                    "hazard_type": hazard_type,
                    "population_exposure": d["population"],
                    "capital_exposure": d["capital"],
                    "pdc": pdc,
                }
                pdc_displacement_list.append(PdcDisplacement(**c_data))

        PdcDisplacement.objects.bulk_create(pdc_displacement_list)

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_DISPLACEMENT)
    def handle(self, **_):

        uuids = Pdc.objects.filter(status=Pdc.Status.ACTIVE).values_list("uuid", "hazard_type", "pdc_updated_at")

        for uuid, hazard_type, pdc_updated_at in uuids:
            if not PdcDisplacement.objects.filter(
                pdc__uuid=uuid,
                pdc__hazard_type=hazard_type,
                pdc__pdc_updated_at=pdc_updated_at,
            ).exists():
                pdc = Pdc.objects.filter(uuid=uuid).last()
                response_data = self.fetch_pdc_data(uuid)

                if response_data:
                    self.create_pdc_displacement(pdc, hazard_type, response_data.get("totalByCountry"))
