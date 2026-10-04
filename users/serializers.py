"""Сериализаторы приложения users."""
from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    password: serializers.CharField = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        """Метаданные сериализатора."""
        model: type = User
        fields: tuple = ("id", "username", "email", "password", "role")
        read_only_fields: tuple = ("id", "role")

    def create(self, validated_data: dict) -> User:
        """Создаёт пользователя с зашифрованным паролем."""
        password: str = validated_data.pop("password")
        user: User = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
