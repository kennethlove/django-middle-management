from django.http import HttpRequest, HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

from ._base import _run_command_view


@api_view(["POST"])
def run_command_view(request: HttpRequest, command: str) -> HttpResponse:
    """Execute a management command from a list of allowed commands.

    Accepts a command name and optional arguments as a JSON body.
    """
    return _run_command_view(request, command)
