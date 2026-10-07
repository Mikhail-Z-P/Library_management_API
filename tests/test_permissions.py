"""Тесты permissions — доступ без авторизации."""

import pytest


@pytest.mark.django_db
def test_unauthorized_access_blocked(api_client: pytest.fixture) -> None:
    """Тест запрета доступа без токена."""
    endpoints: list[str] = [
        "/api/v1/authors/",
        "/api/v1/books/",
        "/api/v1/loans/",
    ]
    for url in endpoints:
        response = api_client.get(url)
        assert response.status_code == 401


@pytest.mark.django_db
def test_swagger_accessible(api_client: pytest.fixture) -> None:
    """Тест доступности Swagger UI без авторизации."""
    response = api_client.get("/api/swagger/")
    assert response.status_code == 200
