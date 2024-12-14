# Django Middle Management

It's usually a bad idea to connect to production servers to run one-off or maintenance
commands. There may not be any auditing, commands and payloads can have mistakes, and
a rogue developer could get away with almost anything. With `django-middle-management`,
though, you don't have to allow shell access so your headaches are reduced.

This is a small library that makes it possible to securely and remotely execute Django
management commands via `POST` requests. Commands must be merged into your code base
before they're eligible to be used. They must also be listed in `settings.py` or they
cannot be triggered. Finally, requests must be authenticated by your system before any
command can be given.

Warning: This project runs management commands remotely but _synchronously_.
Long-running commands will potentially block your server from responding to other requests.
Using a task queue like Celery is recommend for anything that may take more than a few seconds.

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

And, finally, add an allowlist of commands:

```python
MANAGE_ALLOW_LIST = ["noop"]
```

## Usage

To execute a management command, make a `POST` request to the
`/__manage__/<command name>` endpoint with the following JSON payload:

```json
{
    "data": {
        "arg1": "value1",
        "arg2": "value2"
    }
}
```

Your `POST` must also contain a valid `HTTP_AUTHORIZATION` header
with the value `Bearer <token>`.