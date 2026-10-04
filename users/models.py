"""Модели приложения users."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с ролями."""

    class Role(models.TextChoices):
        """Перечисление ролей пользователя."""
        MANAGER = "manager", "Менеджер"
        READER = "reader", "Читатель"

    role: models.CharField = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.READER,
        verbose_name="роль",
    )

    class Meta:
        """Метаданные модели User."""
        verbose_name: str = "пользователь"
        verbose_name_plural: str = "пользователи"

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"{self.username} ({self.role})"
