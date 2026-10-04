"""Сериализаторы приложения library."""
from rest_framework import serializers

from library.models import Author, Book, Loan


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Author."""

    class Meta:
        """Метаданные сериализатора."""
        model: type = Author
        fields: str = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Book."""

    author_name: serializers.ReadOnlyField = serializers.ReadOnlyField(
        source="author.name",
    )

    class Meta:
        """Метаданные сериализатора."""
        model: type = Book
        fields: tuple = (
            "id",
            "title",
            "description",
            "genre",
            "isbn",
            "author",
            "author_name",
            "available",
            "created_at",
        )


class LoanSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Loan."""

    book_title: serializers.ReadOnlyField = serializers.ReadOnlyField(
        source="book.title",
    )
    reader_name: serializers.ReadOnlyField = serializers.ReadOnlyField(
        source="reader.username",
    )

    class Meta:
        """Метаданные сериализатора."""
        model: type = Loan
        fields: tuple = (
            "id",
            "book",
            "book_title",
            "reader",
            "reader_name",
            "loan_date",
            "return_date",
            "is_returned",
        )
        read_only_fields: tuple = ("reader", "loan_date")
