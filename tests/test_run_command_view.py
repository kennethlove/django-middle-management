"""Tests for the run_command view."""
import json
from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse


def has_drf():
    """Check if Django REST Framework is installed."""
    from django.conf import settings
    return "rest_framework" in settings.INSTALLED_APPS

requires_drf = pytest.mark.skipif(
    not has_drf(),
    reason="Django REST Framework is not in `INSTALLED_APPS`, skipping DRF tests."
)

requires_django = pytest.mark.skipif(
    has_drf(),
    reason="Django REST Framework is in `INSTALLED_APPS`, skipping non-DRF tests."
)

@requires_django
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


@requires_django
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


@requires_django
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


@requires_drf
@pytest.mark.drf
@pytest.mark.django_db
@patch("middle_management.views._base.call_command", spec=True)
def test_rest_framework_permission_class(call_command, admin_user):
    """Test that the DRF permission class is applied.

    The view should only be accessible to authenticated users.
    """
    from rest_framework.authtoken.models import Token
    from rest_framework.test import APIClient

    token = Token.objects.create(user=admin_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    url = reverse("manage_run_command", kwargs={"command": "noop"})
    response = client.post(url, data={}, format="json")

    assert response.status_code == 200
    call_command.assert_called_once_with("noop")
