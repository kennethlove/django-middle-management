from django.urls import path
from orm_manage.views import run_command_view

urlpatterns = [
    path("__manage__/<str:command>", run_command_view, name="manage_run_command"),
]

manage_urls = urlpatterns
