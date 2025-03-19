"""Views for the middle management app."""

import json

from django.conf import settings
from django.core.management import call_command
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

ALLOW_LIST: list[str] = (settings.MANAGE_ALLOW_LIST if
                         hasattr(settings, "MANAGE_ALLOW_LIST") else [])


@csrf_exempt
@require_http_methods(["POST"])
def run_command_view(request: HttpRequest, command: str) -> HttpResponse:
    """Execute a management command from a list of allowed commands.

    Accepts a command name, authentication token, and optional arguments as a JSON body.
    """
    if request.user.is_authenticated:
        if command in ALLOW_LIST:
            data = json.loads(request.body)
            call_command(command, **data)
            return HttpResponse("Command executed")
        return HttpResponse("Command not allowed", status=403)
    return HttpResponse("Unauthorized", status=401)
