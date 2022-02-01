from django.core.management.base import BaseCommand

from seasonal.scripts.create_global_data import create_global_displacment_data


class Command(BaseCommand):
    help = 'Create Global Displacement Data'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, **options):
        file = options.get('file')
        create_global_displacment_data(file)
