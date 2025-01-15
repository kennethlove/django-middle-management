from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Does nothing"

    def handle(self, *args, **options):
        pass