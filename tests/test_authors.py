"""Тесты CRUD для авторов."""

import pytest


@pytest.mark.django_db
def test_list_authors(reader_client: pytest.fixture, author: pytest.fixture) -> None:
    """Тест получения списка авторов читателем."""
    response = reader_client.get("/api/v1/authors/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_author_manager(manager_client: pytest.fixture) -> None:
    """Тест создания автора менеджером."""
    response = manager_client.post(
        "/api/v1/authors/",
        {
            "name": "Новый Автор",
            "bio": "Биография",
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["name"] == "Новый Автор"


@pytest.mark.django_db
def test_create_author_forbidden_reader(reader_client: pytest.fixture) -> None:
    """Тест запрета создания автора читателем."""
    response = reader_client.post(
        "/api/v1/authors/",
        {
            "name": "Запрет",
            "bio": "",
        },
        format="json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_author_manager(
    manager_client: pytest.fixture, author: pytest.fixture
) -> None:
    """Тест удаления автора менеджером."""
    url: str = f"/api/v1/authors/{author.id}/"
    response = manager_client.delete(url)
    assert response.status_code == 204
