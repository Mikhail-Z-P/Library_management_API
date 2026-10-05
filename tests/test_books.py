"""Тесты CRUD и фильтрации для книг."""
import pytest


@pytest.mark.django_db
def test_list_books(reader_client: pytest.fixture, book: pytest.fixture) -> None:
    """Тест получения списка книг читателем."""
    response = reader_client.get("/api/v1/books/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_book_manager(manager_client: pytest.fixture, author: pytest.fixture) -> None:
    """Тест создания книги менеджером."""
    response = manager_client.post("/api/v1/books/", {
        "title": "Новая Книга",
        "description": "Описание",
        "genre": "детектив",
        "isbn": "9782222222222",
        "author": author.id,
    }, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_filter_books_by_genre(
    reader_client: pytest.fixture,
    author: pytest.fixture,
) -> None:
    """Тест фильтрации книг по жанру."""
    from library.models import Book
    Book.objects.create(
        title="Книга 1", genre="роман", isbn="111", author=author,
    )
    Book.objects.create(
        title="Книга 2", genre="детектив", isbn="222", author=author,
    )
    response = reader_client.get("/api/v1/books/?genre=роман")
    assert response.status_code == 200
    assert all(b["genre"] == "роман" for b in response.data)


@pytest.mark.django_db
def test_create_book_forbidden_reader(
    reader_client: pytest.fixture,
    author: pytest.fixture,
) -> None:
    """Тест запрета создания книги читателем."""
    response = reader_client.post("/api/v1/books/", {
        "title": "Запрет",
        "genre": "роман",
        "isbn": "999",
        "author": author.id,
    }, format="json")
    assert response.status_code == 403
