import requests
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from imminent.models import Pdc, PdcDisplacement
from common.models import Country

logger = logging.getLogger()


class Command(BaseCommand):
    help = "Import Hazard Exposure Data"

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_DISPLACEMENT)
    def handle(self, *args, **options):

        def fetch_pdc_data(uuid, hazard_type, pdc_updated_at):
            url = f"https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/latest/"
            headers = {"Authorization": f"Bearer {settings.PDC_ACCESS_TOKEN}"}
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                error_log = f"Error querying PDC Exposure data at {url}"
                logger.error(error_log)
                logger.error(response.content)
                return None

            return response.json()

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

        uuids = (
            Pdc.objects
            .filter(status=Pdc.Status.ACTIVE)
            .values_list("uuid", "hazard_type", "pdc_updated_at")
        )

        for uuid, hazard_type, pdc_updated_at in uuids:
            if not PdcDisplacement.objects.filter(
                pdc__uuid=uuid,
                pdc__hazard_type=hazard_type,
                pdc__pdc_updated_at=pdc_updated_at,
            ).exists():
                pdc = Pdc.objects.filter(uuid=uuid).last()
                response_data = fetch_pdc_data(uuid, hazard_type, pdc_updated_at)

                if response_data:
                    create_pdc_displacement(pdc, hazard_type, response_data.get("totalByCountry"))
