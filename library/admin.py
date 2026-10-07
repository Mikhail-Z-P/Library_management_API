"""Админка приложения library."""

from django.contrib import admin

from library.models import Author, Book, Loan


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Админ-конфигурация для Author."""

    list_display: tuple = ("name", "created_at")
    search_fields: tuple = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Админ-конфигурация для Book."""

    list_display: tuple = ("title", "author", "genre", "isbn", "available")
    list_filter: tuple = ("genre", "available")
    search_fields: tuple = ("title", "isbn")


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Админ-конфигурация для Loan."""

    list_display: tuple = ("book", "reader", "loan_date", "return_date", "is_returned")
    list_filter: tuple = ("is_returned",)
