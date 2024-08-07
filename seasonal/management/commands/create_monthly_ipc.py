import pandas as pd
from django.core.management.base import BaseCommand

from common.models import Country
from seasonal.models import EstimationType, Ipc, IpcMonthly


class Command(BaseCommand):
    help = "Create Monthly Ipc from the api pull"

    def handle(self, *args, **options):
        # Create a separate monthly ipc for the object
        queryset = Ipc.objects.all()
        for data in queryset:
            country = data.country.id
            hazard_type = data.hazard_type
            phase_population = data.phase_population
            analysis_date = data.analysis_date
            census_population = data.census_population
            projected_population = data.projected_phase_population
            projected_period_start_date = data.projected_period_start_date
            projected_period_end_date = data.projected_period_end_date
            current_period_start_date = data.current_period_start_date
            current_period_end_date = data.current_period_end_date
            second_projection_period_start_date = data.second_projected_period_start_date
            second_projection_period_end_date = data.second_projected_period_end_date
            # current
            if current_period_start_date and current_period_end_date:
                date_range_current = pd.date_range(current_period_start_date, current_period_end_date, freq="MS")
                for range in date_range_current:
                    year = int(range.strftime("%Y"))
                    month = int(range.strftime("%m"))
                    data = {
                        "country": Country.objects.get(id=country),
                        "hazard_type": hazard_type,
                        "phase_population": phase_population,
                        "year": year,
                        "month": month,
                        "estimation_type": EstimationType.CURRENT,
                        "analysis_date": analysis_date,
                        "census_population": census_population,
                    }
                    IpcMonthly.objects.create(**data)
            # first_projection
            if projected_period_start_date and projected_period_end_date:
                date_range_projected = pd.date_range(projected_period_start_date, projected_period_end_date, freq="MS")
                for range in date_range_projected:
                    year = int(range.strftime("%Y"))
                    month = int(range.strftime("%m"))
                    data = {
                        "country": Country.objects.get(id=country),
                        "hazard_type": hazard_type,
                        "phase_population": projected_population,
                        "year": year,
                        "month": month,
                        "estimation_type": EstimationType.FIRST_PROJECTION,
                        "analysis_date": analysis_date,
                        "census_population": census_population,
                    }
                    IpcMonthly.objects.create(**data)

            # second_projection
            if second_projection_period_start_date and second_projection_period_end_date:
                date_range_projected = pd.date_range(
                    second_projection_period_start_date, second_projection_period_end_date, freq="MS"
                )
                for range in date_range_projected:
                    year = int(range.strftime("%Y"))
                    month = int(range.strftime("%m"))
                    data = {
                        "country": Country.objects.get(id=country),
                        "hazard_type": hazard_type,
                        "phase_population": projected_population,
                        "year": year,
                        "month": month,
                        "estimation_type": EstimationType.SECOND_PROJECTION,
                        "analysis_date": analysis_date,
                        "census_population": census_population,
                    }
                    IpcMonthly.objects.create(**data)
