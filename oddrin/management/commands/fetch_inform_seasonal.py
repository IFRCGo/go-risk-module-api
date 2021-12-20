from django.core.management.base import BaseCommand

from oddrin.scripts.fetch_inform_seasonal import fetch_inform_seasonal


class Command(BaseCommand):
    help = 'Fetch idmc pmd data'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, **options):
        file = options.get('file')
        fetch_inform_seasonal(file)
