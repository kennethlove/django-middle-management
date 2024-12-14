import json
from unittest.mock import patch

from django.urls import reverse


@patch("middle_management.views.call_command", spec=True)
def test_basic_authenticated_usage(call_command, admin_client):
    """A POST request with valid authentication and command name should return a 200 response."""
    headers = {
        "HTTP_AUTHORIZATION": "Bearer some_valid_token",
    }

    data = {"foo": "bar", "baz": "qux"}
    url = reverse("manage_run_command", kwargs={"command": "noop"})

    response = admin_client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
        headers=headers
    )

    assert response.status_code == 200
    call_command.assert_called_once_with("noop", **data)


@patch("middle_management.views.call_command", spec=True)
def test_basic_unauthenticated_usage(call_command, client):
    """A POST request without valid authentication should return a 403 response."""
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "noop"})
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 302
    call_command.assert_not_called()


@patch("middle_management.views.call_command", spec=True)
def test_invalid_command_usage(call_command, admin_client):
    """A POST request with valid authentication but an invalid command name should return a 403 response."""
    headers = {
        "HTTP_AUTHORIZATION": "Bearer some_valid_token",
    }
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "not_a_command"})
    response = admin_client.post(url, data=json.dumps(data), content_type="application/json", **headers)
    assert response.status_code == 403
    call_command.assert_not_called()
