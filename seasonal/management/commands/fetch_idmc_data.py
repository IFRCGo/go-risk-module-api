from django.core.management.base import BaseCommand

from seasonal.scripts.fetch_idmc_data import fetch_idmc_data


class Command(BaseCommand):
    help = "Fetch Idmc Displacement Data"

    def add_arguments(self, parser):
        parser.add_argument("--file")

    def handle(self, **options):
        file = options.get("file")
        fetch_idmc_data(file)
