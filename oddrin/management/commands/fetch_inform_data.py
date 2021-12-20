from django.core.management.base import BaseCommand

from oddrin.scripts.fetch_inform_data import fetch_inform_data


class Command(BaseCommand):
    help = 'Fetch Informa Risk Score Data'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, **options):
        file = options.get('file')
        fetch_inform_data(file)
