from typing import Any

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command that does nothing."""

    help = "Does nothing"

    def handle(self, *args: object, **options: dict[str, Any]) -> None:
        """Handle the command."""