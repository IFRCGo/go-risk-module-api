import requests
import logging
import pandas as pd


from django.core.management.base import BaseCommand

from common.models import HazardType, Country
from common.utils import logging_response_context
from seasonal.models import DisplacementData


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Displacement Data"

    def handle(self, *args, **options):
        DisplacementData.objects.all().delete()
        countries_iso3 = Country.objects.all().values_list("iso3", flat=True)
        for iso3 in countries_iso3:
            if iso3:
                disaster_url = "https://preview.grid.unep.ch/index.php?preview=tools&cat=2&lang=eng"
                data = {
                    "hazardType": "flood",
                    "aggLevel": "byCountry",
                    "cntySelect[]": iso3.upper(),
                    "queryPreview": "Query",
                }
                session = requests.Session()
                response = session.post(disaster_url, data=data)
                if response.status_code != 200:
                    logger.error(
                        "Error querying Displacement data",
                        extra=logging_response_context(response),
                    )
                    # TODO: continue?

                tables = pd.read_html(response.content)
                displacement_data = tables[0]
                if hasattr(displacement_data, "Average modelised physical exposure per year (total x 1000)"):
                    annual_average_displacement = (
                        displacement_data["Average modelised physical exposure per year (total x 1000)"][0] * 1000
                    )
                else:
                    annual_average_displacement = None
                data = {
                    "country": Country.objects.filter(iso3=iso3).first(),
                    "hazard_type": HazardType.FLOOD,
                    "annual_average_displacement": annual_average_displacement,
                    "iso3": iso3,
                }
                DisplacementData.objects.get_or_create(**data)
