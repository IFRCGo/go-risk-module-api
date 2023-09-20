import logging

from django.core.management.base import BaseCommand
from django.db.models import Max, Min, F

from imminent.models import MeteoSwiss, MeteoSwissAgg
from common.models import HazardType, Country

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Aggregated Meteoswiss Data"

    def handle(self, *args, **kwargs):
        def get_latest_meteo_swiss_data(hazard_name, country_name):
            return MeteoSwiss.objects.filter(
                impact_type="exposed_population_18mps",
                hazard_name=hazard_name,
                country__name=country_name
            ).order_by("-initialization_date").first()

        def get_event_details(hazard_name, country_name):
            latest_dates = MeteoSwiss.objects.filter(
                hazard_name=hazard_name,
                country__name=country_name,
            ).values('impact_type').annotate(
                latest_initialization_date=Max('initialization_date')
            )

            latest_data = []
            for item in latest_dates:
                impact_type = item['impact_type']
                latest_date = item['latest_initialization_date']
                latest_data_query = MeteoSwiss.objects.filter(
                    hazard_name=hazard_name,
                    country__name=country_name,
                    impact_type=impact_type,
                    initialization_date=latest_date
                ).values(
                    'impact_type',
                    'id',
                    max=F('event_details__max'),
                    mean=F('event_details__mean'),
                    min=F('event_details__min'),
                )

                latest_data.extend(latest_data_query)

            return list(latest_data)

        def find_country_by_name(country_name):
            return Country.objects.filter(name__icontains=country_name).first() if country_name else None

        def create_meteo_swiss_agg_entry(event, latest_data, event_details):
            country = find_country_by_name(event["country__name"])

            data = {
                "country": country,
                "hazard_name": event["hazard_name"],
                "start_date": event["event_date"],
                "event_details": list(event_details),
                "hazard_type": HazardType.CYCLONE,
                "updated_at": event["initialization_date"],
                "geojson_details": {
                    "id": latest_data.id,
                    "impact_type": latest_data.impact_type,
                    "footprint_geojson": latest_data.footprint_geojson,
                },
            }

            MeteoSwissAgg.objects.create(**data)

        # Get distinct hazard_name and country_name combinations with start_date and end_date
        event_query = MeteoSwiss.objects.filter(
            impact_type="exposed_population_18mps"
        ).values("hazard_name", "country__name").distinct().annotate(
            initialization_date=Min("initialization_date"),
            event_date=Max("event_date"),
        )

        for event in event_query:
            hazard_name = event["hazard_name"]
            country_name = event["country__name"]

            latest_data = get_latest_meteo_swiss_data(hazard_name, country_name)

            if latest_data:
                event_details = get_event_details(hazard_name, country_name)
                create_meteo_swiss_agg_entry(event, latest_data, event_details)
