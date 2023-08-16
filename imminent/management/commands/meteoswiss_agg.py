import logging

from django.core.management.base import BaseCommand
from django.db.models import Max, Min

from imminent.models import MeteoSwiss, MeteoSwissAgg
from common.models import HazardType, Country

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Aggregated Meteoswiss Data"

    def handle(self, *args, **kwargs):
        events = (
            MeteoSwiss.objects.values("hazard_name", "country__name")
            .distinct()
            .annotate(
                start_date=Min("initialization_date"),
                end_date=Max("event_date"),
            )
        )
        for event in list(events):
            # get the footprint_geojson latest
            # what if this has no any polygon
            data = (
                MeteoSwiss.objects.filter(
                    impact_type="exposed_population_18mps",
                    hazard_name=event["hazard_name"],
                    country__name=event["country__name"],
                )
                .order_by("initialization_date")
                .last()
            )
            new_dict = {
                "id": data.id,
                "impact_type": data.impact_type,
                "footprint_geojson": data.footprint_geojson,
            }
            event_details_dict = [
                {
                    "id": data.id,
                    "impact_type": data.impact_type,
                    "max": data.event_details.get("max"),
                    "mean": data.event_details.get("mean"),
                    "min": data.event_details.get("min"),
                }
                for data in MeteoSwiss.objects.filter(
                    hazard_name=event["hazard_name"], country__name=event["country__name"]
                ).order_by("initialization_date")
            ]
            details = {x["impact_type"]: x for x in event_details_dict}.values()
            country_name = event["country__name"]
            if country_name:
                country = Country.objects.filter(name__icontains=event["country__name"]).first()
            else:
                country = None
            data = {
                "country": country,
                "hazard_name": event["hazard_name"],
                "start_date": event["start_date"],
                "event_details": list(details),
                "hazard_type": HazardType.CYCLONE,
                "end_date": event["end_date"],
                "geojson_details": new_dict,
            }
            MeteoSwissAgg.objects.create(**data)