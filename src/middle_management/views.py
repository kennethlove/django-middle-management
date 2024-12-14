import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

ALLOW_LIST: list[str] = settings.MANAGE_ALLOW_LIST if hasattr(settings, "MANAGE_ALLOW_LIST") else []


@login_required()
@require_http_methods(["POST"])
def run_command_view(request, command: str) -> HttpResponse:
    """Execute a management command from a list of allowed commands.

    Accepts a command name, authentication token, and optional arguments as a JSON body.
    """

    if command in ALLOW_LIST:
        data = json.loads(request.body)
        call_command(command, **data)
        return HttpResponse("Command executed")
    return HttpResponse("Command not allowed", status=403)
