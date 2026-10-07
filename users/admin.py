"""Админка приложения users."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админ-конфигурация для кастомной модели User."""

    list_display: tuple = ("username", "email", "role", "is_staff")
    list_filter: tuple = ("role", "is_staff", "is_active")
    fieldsets: tuple = UserAdmin.fieldsets + (("Роль", {"fields": ("role",)}),)
