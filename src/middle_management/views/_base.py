"""Views for the middle management app."""

import json

from django.conf import settings
from django.core.management import call_command
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
)
from django.views.decorators.http import require_http_methods

ALLOW_LIST: list[str] = (
    settings.MANAGE_ALLOW_LIST if hasattr(settings, "MANAGE_ALLOW_LIST") else []
)


@require_http_methods(["POST"])
def _run_command_view(request: HttpRequest, command: str) -> HttpResponse:
    """Execute a management command from a list of allowed commands.

    Accepts a command name, authentication token, and optional arguments as a JSON body.
    """
    if command in ALLOW_LIST:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        else:
            call_command(command, **data)
            return HttpResponse()
    return HttpResponseBadRequest("Unknown command")