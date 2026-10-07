"""Тесты выдач книг и возврата."""

import pytest


@pytest.mark.django_db
def test_create_loan_reader(
    reader_client: pytest.fixture,
    reader: pytest.fixture,
    book: pytest.fixture,
) -> None:
    """Тест создания выдачи читателем — reader подставляется автоматически."""
    response = reader_client.post(
        "/api/v1/loans/",
        {
            "book": book.id,
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["reader"] == reader.id
    assert response.data["is_returned"] is False


@pytest.mark.django_db
def test_create_loan_unavailable_book(
    reader_client: pytest.fixture,
    book: pytest.fixture,
) -> None:
    """Тест невозможности выдачи недоступной книги — проверяется логикой."""
    book.available = False
    book.save()
    response = reader_client.post(
        "/api/v1/loans/",
        {
            "book": book.id,
        },
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_return_book_manager(
    manager_client: pytest.fixture,
    book: pytest.fixture,
    reader: pytest.fixture,
) -> None:
    """Тест возврата книги менеджером через кастомный action."""
    from library.models import Loan

    loan: Loan = Loan.objects.create(book=book, reader=reader)
    url: str = f"/api/v1/loans/{loan.id}/return_book/"
    response = manager_client.post(url)
    assert response.status_code == 200
    loan.refresh_from_db()
    assert loan.is_returned is True


@pytest.mark.django_db
def test_return_book_forbidden_reader(
    reader_client: pytest.fixture,
    book: pytest.fixture,
    reader: pytest.fixture,
) -> None:
    """Тест запрета возврата книги читателем."""
    from library.models import Loan

    loan: Loan = Loan.objects.create(book=book, reader=reader)
    url: str = f"/api/v1/loans/{loan.id}/return_book/"
    response = reader_client.post(url)
    assert response.status_code == 403
