import logging

import requests
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.utils import logging_response_context
from imminent.models import Pdc, PdcDisplacement
from imminent.sources.pdc import SentryPdcSource
from imminent.sources.utils import CountryQuery
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Hazard Exposure Data"

    @staticmethod
    def fetch_pdc_data(uuid):
        response = requests.get(
            SentryPdcSource.URL.get_hazard_exposure_latest(uuid),
            headers=SentryPdcSource.authorization_headers(),
        )

        if response.status_code != 200:
            logger.error(
                "Error querying PDC Exposure data",
                extra=logging_response_context(response),
            )
            return None

        return response.json()

    @staticmethod
    def create_pdc_displacement(country_query: CountryQuery, pdc: Pdc, total_by_country_data):
        pdc_displacement_list = []

        for d in total_by_country_data:
            iso3 = d["country"].lower()
            if country := country_query.get_by_iso3(iso3):
                c_data = {
                    "country": country,
                    "hazard_type": pdc.hazard_type,
                    "pdc": pdc,
                    "population_exposure": d["population"],
                    "capital_exposure": d["capital"],
                }
                pdc_displacement_list.append(PdcDisplacement(**c_data))

        PdcDisplacement.objects.bulk_create(pdc_displacement_list)

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_DISPLACEMENT)
    def handle(self, **_):

        country_query = CountryQuery()
        pdc_qs = Pdc.objects.filter(
            status=Pdc.Status.ACTIVE,
            stale_displacement=True,
        )

        for pdc in pdc_qs:
            PdcDisplacement.objects.filter(pdc=pdc).delete()
            if response_data := self.fetch_pdc_data(pdc.uuid):
                self.create_pdc_displacement(country_query, pdc, response_data.get("totalByCountry"))
            pdc.stale_displacement = False
            pdc.save(update_fields=("stale_displacement",))
