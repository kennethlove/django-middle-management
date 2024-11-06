# ORM Manage

Small library to it possible to securely and remotely execute Django management commands.

Note: This is a work in progress and is not yet ready for production use.

Warning: This project runs commands synchronously. Long-running commands will block the server.

## Installation

```bash
pip install git+https://github.com/kennethlove/orm-manage.git
```

or, once released,

```bash
pip install orm-manage
```


Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'orm_manage',
    ...
]
```

Add the URLs to your project's `urls.py`:

```python
from orm_manage.urls import manage_urls

urlpatterns = [
    ...
] + manage_urls
```

## Usage

To execute a management command, make a `POST` request to the `/__manage__/<command name>` endpoint with the following JSON payload:

```json
{
    "data": {
        "arg1": "value1",
        "arg2": "value2"
    }
}
```

Your `POST` must also contain a valid `HTTP_AUTHORIZATION` header with the value `Bearer <token>`.