"""Фильтры для API библиотеки."""

import django_filters

from library.models import Book


class BookFilter(django_filters.FilterSet):
    """Фильтр для книг по жанру, автору и доступности."""

    class Meta:
        """Метаданные фильтра."""

        model: type = Book
        fields: dict = {
            "genre": ["exact", "icontains"],
            "author": ["exact"],
            "available": ["exact"],
        }
