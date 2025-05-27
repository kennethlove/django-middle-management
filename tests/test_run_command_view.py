"""Tests for the run_command view."""
import json
from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse


@patch("middle_management.views._base.call_command", spec=True)
def test_basic_authenticated_usage(call_command, admin_user):
    """Test a valid command name with an authenticated user.

    A POST request with valid authentication and command name should return
    a 200 response.
    """
    client = Client(enforce_csrf_checks=True)
    client.force_login(user=admin_user)

    data = {}
    url = reverse("manage_run_command", kwargs={"command": "noop"})

    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    call_command.assert_called_once_with("noop")


@patch("middle_management.views._base.call_command", spec=True)
def test_basic_unauthenticated_usage(call_command, client):
    """Test a valid command with an unauthenticated user.

    A POST request without valid authentication should return a 302 response.
    """
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "noop"})
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 302
    call_command.assert_not_called()


@patch("middle_management.views._base.call_command", spec=True)
def test_invalid_command_usage(call_command, admin_client):
    """Test a non-existent command name.

    A POST request with valid authentication but an invalid command name should
    return a 403 response.
    """
    headers = {
        "HTTP_AUTHORIZATION": "Bearer some_valid_token",
    }
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "not_a_command"})
    response = admin_client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
        **headers
    )
    assert response.status_code == 400
    call_command.assert_not_called()

def has_drf():
    """Check if Django REST Framework is installed."""
    try:
        import rest_framework  # noqa: F401
    except ImportError:
        return False
    else:
        return True

requires_drf = pytest.mark.skipif(
    not has_drf(),
    reason="Django REST Framework is not installed, skipping DRF tests."
)

@requires_drf
@pytest.mark.drf
@pytest.mark.django_db(transaction=True)
@patch("middle_management.views._base.call_command", spec=True)
def test_rest_framework_permission_class(call_command, admin_user, settings):
    """Test that the DRF permission class is applied.

    The view should only be accessible to authenticated users.
    """
    settings.INSTALLED_APPS += [
        "rest_framework",
        "rest_framework.authtoken",
    ]

    from django.db import connection
    from rest_framework.authtoken.models import Token
    from rest_framework.test import APIClient

    with connection.schema_editor() as editor:
        editor.create_model(Token)

    token = Token.objects.create(user=admin_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    url = reverse("manage_run_command", kwargs={"command": "noop"})
    response = client.post(url, format="json")

    assert response.status_code == 200
    call_command.assert_called_once_with("noop")
