"""URL-роуты приложения library."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from library.views import AuthorViewSet, BookViewSet, LoanViewSet


router: DefaultRouter = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="book")
router.register(r"loans", LoanViewSet, basename="loan")


urlpatterns: list = [
    path("", include(router.urls)),
]
