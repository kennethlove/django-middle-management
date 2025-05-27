"""Views for the middle management app."""

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from ._base import _run_command_view

run_command_view = csrf_exempt(login_required(_run_command_view))
