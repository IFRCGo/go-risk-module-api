from django.core.management.base import BaseCommand

from oddrin.scripts.create_exposure_population import create_exposure_population


class Command(BaseCommand):
    help = "Create Global Population Exposure"

    def add_arguments(self, parser):
        parser.add_argument("--file")

    def handle(self, **options):
        file = options.get("file")
        create_exposure_population(file)
