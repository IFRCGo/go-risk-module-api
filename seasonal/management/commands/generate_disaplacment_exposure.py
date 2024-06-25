# TODO: Clean-up
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Check for displacement higher than exposure'

    def handle(self, *args, **kwargs):
        # list down the  displacement and exposure population for the hazard specific and countrywise
        # this data comes from `Global Risk Data Platform`
        ...
