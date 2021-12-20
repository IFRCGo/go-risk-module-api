from django.core.management.base import BaseCommand

from oddrin.scripts.create_gar_data import create_gar_data


class Command(BaseCommand):
    help = 'Create Global Displacement Data'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, **options):
        file = options.get('file')
        create_gar_data(file)
