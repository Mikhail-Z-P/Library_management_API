"""Общие fixtures для тестов."""

import pytest
from rest_framework.test import APIClient

from library.models import Author, Book
from users.models import User


@pytest.fixture
def api_client() -> APIClient:
    """Возвращает неавторизованный API-клиент."""
    return APIClient()


@pytest.fixture
def manager() -> User:
    """Создаёт пользователя-менеджера."""
    return User.objects.create_user(
        username="manager1",
        email="manager@test.com",
        password="ManagerPass123",
        role="manager",
    )


@pytest.fixture
def reader() -> User:
    """Создаёт пользователя-читателя."""
    return User.objects.create_user(
        username="reader1",
        email="reader@test.com",
        password="ReaderPass123",
        role="reader",
    )


@pytest.fixture
def manager_client(manager: User) -> APIClient:
    """Возвращает API-клиент, авторизованный как менеджер."""
    client: APIClient = APIClient()
    client.force_authenticate(user=manager)
    return client


@pytest.fixture
def reader_client(reader: User) -> APIClient:
    """Возвращает API-клиент, авторизованный как читатель."""
    client: APIClient = APIClient()
    client.force_authenticate(user=reader)
    return client


@pytest.fixture
def author() -> Author:
    """Создаёт автора."""
    return Author.objects.create(name="Тест Автор", bio="Биография")


@pytest.fixture
def book(author: Author) -> Book:
    """Создаёт книгу."""
    return Book.objects.create(
        title="Тест Книга",
        description="Описание",
        genre="роман",
        isbn="9781111111111",
        author=author,
        available=True,
    )
