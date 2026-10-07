"""Конфигурация приложения users."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Конфигурация приложения пользователей."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "users"
