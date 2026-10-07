"""Представления приложения library."""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from library.filters import BookFilter
from library.models import Author, Book, Loan
from library.permissions import IsManager, IsReaderOrCreateOrManager, IsReaderOrManager
from library.serializers import AuthorSerializer, BookSerializer, LoanSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet для авторов: полный CRUD для менеджеров, чтение для читателей."""

    queryset: type = Author.objects.all()
    serializer_class: type = AuthorSerializer
    permission_classes: list = [IsReaderOrManager]


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet для книг с фильтрацией."""

    queryset: type = Book.objects.select_related("author").all()
    serializer_class: type = BookSerializer
    permission_classes: list = [IsReaderOrManager]
    filterset_class: type = BookFilter


class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet для выдач книг."""

    queryset: type = Loan.objects.select_related("book", "reader").all()
    serializer_class: type = LoanSerializer
    permission_classes: list = [IsReaderOrCreateOrManager]

    def perform_create(self, serializer: LoanSerializer) -> None:
        """Создаёт выдачу, подставляя читателя из запроса, и помечает книгу недоступной."""
        loan: Loan = serializer.save(reader=self.request.user)
        loan.book.available = False
        loan.book.save(update_fields=["available"])

    @action(detail=True, methods=["post"], permission_classes=[IsManager])
    def return_book(self, request, pk: int = None) -> Response:
        """Отмечает книгу как возвращённую."""
        loan: Loan = self.get_object()
        if loan.is_returned:
            return Response(
                {"detail": "Книга уже возвращена."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        loan.is_returned = True
        loan.book.available = True
        loan.book.save(update_fields=["available"])
        loan.save(update_fields=["is_returned"])
        return Response({"detail": "Книга возвращена."}, status=status.HTTP_200_OK)
