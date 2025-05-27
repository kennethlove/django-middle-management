"""Views for the middle management app."""

from django.conf import settings

if "rest_framework" in settings.INSTALLED_APPS:
    from ._restframework import run_command_view
else:
    from ._django import run_command_view

__all__ = ["run_command_view"]
