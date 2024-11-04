import json
import os

from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

ALLOW_LIST: list[str] = settings.MANAGE_ALLOW_LIST if hasattr(settings, "MANAGE_ALLOW_LIST") else []


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def run_command_view(request, command: str) -> HttpResponse:
    """Execute a management command from a list of allowed commands.

    Accepts a command name, authentication token, and optional arguments as a JSON body.
    """

    body = json.loads(request.POST.get("data", "{}"))

    if command in ALLOW_LIST:
        call_command(command, **body)
        return HttpResponse("Command executed")
    return HttpResponse("Command not allowed", status=403)
