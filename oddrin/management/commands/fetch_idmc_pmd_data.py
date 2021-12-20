from django.core.management.base import BaseCommand

from oddrin.scripts.fetch_idmc_pmd_data import fetch_idmc_pmd_data


class Command(BaseCommand):
    help = 'Fetch idmc pmd data'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, **options):
        file = options.get('file')
        fetch_idmc_pmd_data(file)
