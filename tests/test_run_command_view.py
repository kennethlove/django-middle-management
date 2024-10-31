from django.urls import reverse
from unittest.mock import patch


@patch("orm_manage.views.call_command")
def test_basic_usage(call_command, client):
    """A POST request with a valid header and command name should return a 200 response."""
    headers = {
        "HTTP_AUTHORIZATION": "Bearer some_token",
    }
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "check"})
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
    assert call_command.called_once_with("check", **data)
