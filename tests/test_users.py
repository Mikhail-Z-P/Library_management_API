"""Тесты для эндпоинтов пользователей."""

import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def api_client() -> APIClient:
    """Фикстура API-клиента."""
    return APIClient()


@pytest.fixture
def reader() -> User:
    """Фикстура читателя."""
    return User.objects.create_user(
        username="reader1",
        email="reader@test.com",
        password="ReaderPass123",
        role="reader",
    )


@pytest.fixture
def manager() -> User:
    """Фикстура менеджера."""
    return User.objects.create_user(
        username="manager1",
        email="manager@test.com",
        password="ManagerPass123",
        role="manager",
    )


@pytest.mark.django_db
def test_register_user(api_client: pytest.fixture) -> None:
    """Тест успешной регистрации нового пользователя."""
    response = api_client.post(
        "/api/v1/users/register/",
        {
            "username": "newuser",
            "email": "new@test.com",
            "password": "NewPass123",
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["username"] == "newuser"
    assert response.data["role"] == "reader"
    assert "password" not in response.data


@pytest.mark.django_db
def test_login_returns_tokens(api_client: pytest.fixture, reader: User) -> None:
    """Тест получения JWT-токенов при логине."""
    response = api_client.post(
        "/api/v1/users/login/",
        {
            "username": "reader1",
            "password": "ReaderPass123",
        },
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_register_duplicate_username(
    api_client: pytest.fixture, reader: User
) -> None:
    """Тест ошибки при дублировании username."""
    response = api_client.post(
        "/api/v1/users/register/",
        {
            "username": "reader1",
            "email": "other@test.com",
            "password": "OtherPass123",
        },
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_me_endpoint(api_client: pytest.fixture, reader: User) -> None:
    """Тест получения профиля текущего пользователя."""
    api_client.force_authenticate(user=reader)
    response = api_client.get("/api/v1/users/me/")
    assert response.status_code == 200
    assert response.data["username"] == "reader1"
    assert response.data["role"] == "reader"


@pytest.mark.django_db
def test_me_unauthorized(api_client: pytest.fixture) -> None:
    """Тест доступа к профилю без токена."""
    response = api_client.get("/api/v1/users/me/")
    assert response.status_code == 401
