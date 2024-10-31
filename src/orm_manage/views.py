import json
import os

from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponse

ALLOW_LIST: list[str] = settings.MANAGE_ALLOW_LIST if hasattr(settings, "MANAGE_ALLOW_LIST") else []


def run_command_view(request, command: str) -> HttpResponse:
    """Execute a management command from a list of allowed commands.

    Accepts a command name, authentication token, and optional arguments as a JSON body.
    """

    token = request.headers.get("Authorization")
    body = json.loads(request.POST.get("data", "{}"))

    if command in ALLOW_LIST:
        data = " ".join([f"--{key} {value}" for key, value in body.items()])
        command_to_run = f"python manage.py {command} {data}"
        call_command(command, **body)
        return HttpResponse("Command executed")
    return HttpResponse("Command not allowed", status=403)
