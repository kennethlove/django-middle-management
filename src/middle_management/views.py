"""Views for the middle management app."""

import json

from django.conf import settings
from django.core.management import call_command
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

ALLOW_LIST: list[str] = (
    settings.MANAGE_ALLOW_LIST if hasattr(settings, "MANAGE_ALLOW_LIST") else []
)


@csrf_exempt
@require_http_methods(["POST"])
def run_command_view(request: HttpRequest, command: str) -> HttpResponse:
    """Execute a management command from a list of allowed commands.

    Accepts a command name, authentication token, and optional arguments as a JSON body.
    """
    if request.user.is_authenticated:
        if command in ALLOW_LIST:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return HttpResponseBadRequest("Bad JSON")
            else:
                call_command(command, **data)
                return HttpResponse()
        return HttpResponseBadRequest()
    return HttpResponseForbidden()


if "rest_framework" in settings.INSTALLED_APPS:
    try:
        from rest_framework.authentication import TokenAuthentication
        from rest_framework.decorators import (
            api_view,
            authentication_classes,
            permission_classes,
        )
        from rest_framework.permissions import IsAuthenticated
    except ImportError:
        pass
    else:
        run_command_view = authentication_classes([TokenAuthentication])(
            run_command_view
        )
        run_command_view = permission_classes([IsAuthenticated])(run_command_view)
        run_command_view = api_view(["POST"])(run_command_view)
