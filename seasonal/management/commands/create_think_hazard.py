from django.core.management.base import BaseCommand

from seasonal.scripts.create_think_hazard import create_think_hazard


class Command(BaseCommand):
    help = 'Create ThinkHazardInformation'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, **options):
        file = options.get('file')
        create_think_hazard(file)
