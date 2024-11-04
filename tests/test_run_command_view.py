from django.urls import reverse
from unittest.mock import patch


@patch("orm_manage.views.call_command")
def test_basic_authenticated_usage(call_command, admin_client):
    """A POST request with valid authentication and command name should return a 200 response."""

    headers = {
        "HTTP_AUTHORIZATION": "Bearer some_valid_token",
    }
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "check"})
    response = admin_client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert call_command.called_once_with("check", **data)


@patch("orm_manage.views.call_command")
def test_basic_unauthenticated_usage(call_command, client):
    """A POST request without valid authentication should return a 200 response."""

    data = {}
    url = reverse("manage_run_command", kwargs={"command": "check"})
    response = client.post(url, data=data)
    assert response.status_code == 403
    assert call_command.not_called()


@patch("orm_manage.views.call_command")
def test_invalid_command_usage(call_command, admin_client):
    """A POST request with valid authentication but an invalid command name should return a 403 response."""

    headers = {
        "HTTP_AUTHORIZATION": "Bearer some_valid_token",
    }
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "not_a_command"})
    response = admin_client.post(url, data=data, **headers)
    assert response.status_code == 403
    assert call_command.not_called()
