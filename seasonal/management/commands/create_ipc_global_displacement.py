from django.core.management.base import BaseCommand
from django.db import models

from seasonal.models import (
    IpcMonthly,
    GlobalDisplacement,
)
from common.models import Country


class Command(BaseCommand):
    help = 'Create global displacement from ipc for food_insecurity'

    def handle(self, *args, **options):
        queryset = IpcMonthly.objects.filter(analysis_date__gte='2022-01-01',phase_population__isnull=False).distinct()
        queryset = queryset.values('country', 'analysis_date').annotate(
            total_displacement=models.Sum('phase_population')
        ).values(
            'total_displacement',
            'country_id',
            'hazard_type',
            'analysis_date',
            'year',
            'month',
            'estimation_type',
        )
        for d in queryset:
            data = {
                'country': Country.objects.get(id=d['country_id']),
                'total_displacement': d['total_displacement'],
                'hazard_type': d['hazard_type'],
                'year': d['year'],
                'month': d['month'],
                'estimation_type': d['estimation_type'],
                'analysis_date': d['analysis_date']
            }
            GlobalDisplacement.objects.get_or_create(**data)
