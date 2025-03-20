"""Tests for the run_command view."""
import json
from unittest.mock import patch

from django.test import Client, modify_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@patch("middle_management.views.call_command", spec=True)
def test_basic_authenticated_usage(call_command, admin_user):
    """Test a valid command name with an authenticated user.

    A POST request with valid authentication and command name should return
    a 200 response.
    """
    headers = {
        "HTTP_AUTHORIZATION": "Bearer some_valid_token",
    }

    client = Client(enforce_csrf_checks=True)
    client.force_login(user=admin_user)

    data = {"foo": "bar", "baz": "qux"}
    url = reverse("manage_run_command", kwargs={"command": "noop"})

    response = client.post(
        url, data=json.dumps(data), content_type="application/json", headers=headers
    )

    assert response.status_code == 200
    call_command.assert_called_once_with("noop", **data)


@patch("middle_management.views.call_command", spec=True)
def test_basic_unauthenticated_usage(call_command, client):
    """Test a valid command with an unauthenticated user.

    A POST request without valid authentication should return a 403 response.
    """
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "noop"})
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 403
    call_command.assert_not_called()


@patch("middle_management.views.call_command", spec=True)
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


@patch("middle_management.views.call_command", spec=True)
def test_rest_framework_permission_class(call_command, admin_user, settings):
    """Test that the DRF permission class is applied.

    The view should only be accessible to authenticated users.
    """

    settings.INSTALLED_APPS += [
        "rest_framework",
        "rest_framework.authtoken",
    ]
    token = Token.objects.create(user=admin_user)
    headers = {
        "Authorization": f"Token {token.key}",
    }

    client = APIClient()

    data = {"foo": "bar", "baz": "qux"}
    url = reverse("manage_run_command", kwargs={"command": "noop"})

    response = client.post(
        url, data=json.dumps(data), content_type="application/json", headers=headers
    )

    assert response.status_code == 200
    call_command.assert_called_once_with("noop", **data)
