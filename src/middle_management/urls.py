"""URLS for the middle_management app."""

from django.urls import path

from middle_management.views import run_command_view

urlpatterns = [
    path("__manage__/<str:command>", run_command_view, name="manage_run_command"),
]

manage_urls = urlpatterns
