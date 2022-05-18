from django.core.management.base import BaseCommand

from seasonal.scripts.create_possible_actions import create_possible_actions


class Command(BaseCommand):
    help = 'Possible actions load'

    def add_arguments(self, parser):
        parser.add_argument('--file')

    def handle(self, **options):
        file = options.get('file')
        create_possible_actions(file)
