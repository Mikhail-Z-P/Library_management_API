"""Тесты регистрации и JWT-авторизации."""
import pytest
from users.models import User


@pytest.mark.django_db
def test_register_user(api_client: pytest.fixture) -> None:
    """Тест успешной регистрации нового пользователя."""
    response = api_client.post("/api/v1/auth/register/", {
        "username": "newuser",
        "email": "new@test.com",
        "password": "NewPass123",
    }, format="json")
    assert response.status_code == 201
    assert response.data["username"] == "newuser"
    assert response.data["role"] == "reader"
    assert "password" not in response.data


@pytest.mark.django_db
def test_login_returns_tokens(api_client: pytest.fixture, reader: User) -> None:
    """Тест получения JWT-токенов при логине."""
    response = api_client.post("/api/v1/auth/login/", {
        "username": "reader1",
        "password": "ReaderPass123",
    }, format="json")
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_register_duplicate_username(api_client: pytest.fixture, reader: User) -> None:
    """Тест ошибки при дублировании username."""
    response = api_client.post("/api/v1/auth/register/", {
        "username": "reader1",
        "email": "other@test.com",
        "password": "OtherPass123",
    }, format="json")
    assert response.status_code == 400
