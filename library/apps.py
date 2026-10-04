"""Конфигурация приложения library."""
from django.apps import AppConfig


class LibraryConfig(AppConfig):
    """Конфигурация приложения библиотеки."""
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "library"
