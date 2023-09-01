import pandas as pd
from collections import defaultdict

from django.core.management.base import BaseCommand

from imminent.models import Adam
from common.models import HazardType


class Command(BaseCommand):
    help = "WFP Adam csv population"

    def handle(self, **options):
        adam_population = Adam.objects.filter(
            event_details__isnull=False,
            hazard_type=HazardType.CYCLONE,
        ).order_by("-publish_date", "country") \
        .distinct("country", "publish_date")
        pop_country_dict = defaultdict(list)
        for adam in adam_population:
            try:
                file = adam.event_details.get("url", {}).get("population_csv")
                if file:
                    dataframe = pd.read_csv(file)
                    exposure_dict = {}
                    for speed in ['60_KMH', '90_KMH', '120_KMH']:
                        column_name = f"POP_{speed}"
                        if column_name in dataframe.columns:
                            pop_country = dataframe.groupby(['ADM0_NAME'])[column_name].agg('sum').to_dict()
                            exposure_dict[f'exposure_{speed.lower()}'] = pop_country.get(adam.country.name, None)
                        else:
                            exposure_dict[f'exposure_{speed.lower()}'] = None
                    adam.population_exposure = exposure_dict
                    adam.save(update_fields=["population_exposure"])
            except Exception as e:
                print(e)
