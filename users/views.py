"""Представления приложения users."""
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import User
from users.serializers import UserRegisterSerializer


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    queryset: type = User.objects.all()
    serializer_class: type = UserRegisterSerializer
    permission_classes: list = [AllowAny]
