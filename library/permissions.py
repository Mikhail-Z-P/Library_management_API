"""Кастомные права доступа."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsManager(BasePermission):
    """Доступ только для пользователей с ролью manager."""

    def has_permission(self, request, view) -> bool:
        """Проверяет, что пользователь — менеджер."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "manager"
        )


class IsReaderOrManager(BasePermission):
    """Читатель — только чтение, менеджер — полный доступ."""

    def has_permission(self, request, view) -> bool:
        """Проверяет права по методу запроса и роли."""
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == "manager"


class IsReaderOrCreateOrManager(BasePermission):
    """Читатель — чтение и создание выдачи, менеджер — полный доступ."""

    def has_permission(self, request, view) -> bool:
        """Чтение и POST доступны всем аутентифицированным, остальное — менеджеру."""
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return True
        return request.user.role == "manager"
