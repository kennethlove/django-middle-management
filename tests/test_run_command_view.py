from django.urls import reverse


def test_basic_usage(client):
    """A POST request with a valid header and command name should return a 200 response."""
    headers = {
        "HTTP_AUTHORIZATION": "Bearer some_token",
    }
    data = {}
    url = reverse("manage_run_command", kwargs={"command": "check"})
    response = client.post(url, data=data, **headers)
    assert response.status_code == 200
