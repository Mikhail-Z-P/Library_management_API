"""Модели приложения library."""

from django.conf import settings
from django.db import models


class Author(models.Model):
    """Модель автора книги."""

    name: models.CharField = models.CharField(
        max_length=200,
        verbose_name="имя автора",
    )
    bio: models.TextField = models.TextField(
        blank=True,
        verbose_name="биография",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
    )

    class Meta:
        """Метаданные модели Author."""

        verbose_name: str = "автор"
        verbose_name_plural: str = "авторы"
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """Строковое представление автора."""
        return self.name


class Book(models.Model):
    """Модель книги."""

    title: models.CharField = models.CharField(
        max_length=300,
        verbose_name="название",
    )
    description: models.TextField = models.TextField(
        blank=True,
        verbose_name="описание",
    )
    genre: models.CharField = models.CharField(
        max_length=100,
        verbose_name="жанр",
    )
    isbn: models.CharField = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="ISBN",
    )
    author: models.ForeignKey = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="автор",
    )
    available: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="доступна",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
    )

    class Meta:
        """Метаданные модели Book."""

        verbose_name: str = "книга"
        verbose_name_plural: str = "книги"
        ordering: list[str] = ["title"]

    def __str__(self) -> str:
        """Строковое представление книги."""
        return f"{self.title} — {self.author.name}"


class Loan(models.Model):
    """Модель выдачи книги читателю."""

    book: models.ForeignKey = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="loans",
        verbose_name="книга",
    )
    reader: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loans",
        verbose_name="читатель",
    )
    loan_date: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата выдачи",
    )
    return_date: models.DateTimeField = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="дата возврата",
    )
    is_returned: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="возвращена",
    )

    class Meta:
        """Метаданные модели Loan."""

        verbose_name: str = "выдача"
        verbose_name_plural: str = "выдачи"
        ordering: list[str] = ["-loan_date"]

    def __str__(self) -> str:
        """Строковое представление выдачи."""
        status: str = "возвращена" if self.is_returned else "на руках"
        return f"{self.book.title} — {self.reader.username} ({status})"
