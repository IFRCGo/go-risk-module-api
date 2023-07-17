from django.core.management.base import BaseCommand

from seasonal.scripts.update_gar_data import update_gar_data


class Command(BaseCommand):
    help = "Update Global Displacement Data Economic Losses And Population Exposure"

    def add_arguments(self, parser):
        parser.add_argument("--file")

    def handle(self, **options):
        file = options.get("file")
        update_gar_data(file)
