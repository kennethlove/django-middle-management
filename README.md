# Django Middle Management

It's usually a bad idea to connect to production servers to run one-off or repetitive
maintenance commands. There may not be any auditing, commands and payloads can easily
have mistakes, and a rogue developer could get away with almost anything. With
`django-middle-management`, though, you don't have to allow shell access to your
production servers while still being able to run commands on them.

This is a small library that makes it possible to securely and remotely execute Django
management commands via `POST` requests. Commands must be merged into your code base
before they're eligible to be used. They must also be listed in `settings.py` or they
cannot be triggered. Finally, requests must be authenticated by your system before any
command can be given.

**Warning:** This project runs management commands remotely but _synchronously_.
Long-running commands will potentially block your server from responding to other requests.
Using a task queue like Celery is recommend for anything that may take more than a few
milliseconds.

## Installation

```bash
pip install django-middle-management
```


Add the package to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "middle_management",
    ...
]
```

Add the URLs to your project's `urls.py`:

```python
from middle_management.urls import manage_urls

urlpatterns = [
    ...
] + manage_urls
```

You'll need to write a new management command or select an
existing one to expose. Finally, add that command name to
an allowlist of commands in `settings.py`:

```python
MANAGE_ALLOW_LIST = ["noop"]
```

## Usage

To execute a management command, make a `POST` request to the
`/__manage__/<command name>` endpoint with a payload similar to
the following:

```json
{
    "data": {
        "arg1": "value1",
        "arg2": "value2"
    }
}
```

Your `POST` must also contain a valid `HTTP_AUTHORIZATION` header
with the value `Bearer <token>`. The final request will look
something like:

```shell
curl -XPOST \
  -H 'Authorization: Bearer not-a-real-token' \
  -H "Content-type: application/json" \
  -d '{"data": { "arg1": "value1", "arg2": "value2" }}' \
  'https://example.com/__manage__/noop'
```
