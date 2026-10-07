"""Представления приложения users."""
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserRegisterSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    queryset: type = User.objects.all()
    serializer_class: type = UserRegisterSerializer
    permission_classes: list = [AllowAny]


class MeView(generics.RetrieveAPIView):
    """Профиль текущего пользователя."""

    serializer_class: type = UserProfileSerializer
    permission_classes: list = [IsAuthenticated]

    def get_object(self) -> User:
        """Возвращает текущего пользователя."""
        return self.request.user
