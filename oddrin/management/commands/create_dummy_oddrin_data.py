import os

from django.core.management.base import BaseCommand
from oddrin.models import Oddrin
from oddrin.factories import OddrinFactory, RiskFileFactory


class Command(BaseCommand):
    help = 'Create Dummy Oddrin Data for earthquake'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, *args, **options):
        from ipc.models import Country

        file = options.get('file')
        # Delete all existing Oddrin Data
        self.stdout.write('Deleting Old Oddrin Data')
        Oddrin.objects.all().delete()
        # Creating Oddrin Data
        self.stdout.write('Creating New Oddrin Data')
        # list all the country with the iso3
        countries_iso3_list = []
        for iso3 in Country.objects.values_list('iso3', flat=True):
            countries_iso3_list.append(iso3)
        for iso3 in countries_iso3_list:
            oddrin = OddrinFactory.create(iso3=iso3)
            oddrin.file = RiskFileFactory.create(file=file)
            oddrin.save(update_fields=['file'])
