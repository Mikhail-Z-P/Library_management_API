# Library Management API

REST API для управления библиотекой: авторы, книги, выдачи. Аутентификация через JWT, ролевая модель (менеджер / читатель), фильтрация, OpenAPI-документация.

## Стек

| Категория | Технологии |
|-----------|------------|
| Backend | Django 5.2, DRF, ORM |
| Auth | djangorestframework-simplejwt |
| Docs | drf-spectacular (Swagger + ReDoc) |
| Filters | django-filter |
| DB | PostgreSQL 16 |
| Контейнеризация | Docker, Docker Compose |
| Зависимости | Poetry |
| Тесты | pytest, pytest-django, pytest-cov (покрытие 95%) |
| Прочее | CORS, python-dotenv, PEP 8 |

## Модели

### User (кастомный, AbstractUser)
- `role` — роль пользователя: `manager` или `reader` (по умолчанию `reader`)

### Author
- `name` — имя автора
- `bio` — биография (текст)

### Book
- `title` — название
- `description` — описание
- `genre` — жанр
- `isbn` — ISBN
- `author` — FK на Author
- `available` — доступна ли книга (bool, по умолчанию `True`)
- `created_at` — дата создания записи

### Loan
- `book` — FK на Book
- `reader` — FK на User
- `loan_date` — дата выдачи (автоматически)
- `return_date` — плановная дата возврата
- `is_returned` — возвращена ли книга (bool, по умолчанию `False`)

## Роли и права доступа

| Действие | Manager | Reader |
|----------|---------|--------|
| Просмотр авторов, книг, выдач | ✅ | ✅ |
| Создание / редактирование авторов | ✅ | ❌ |
| Создание / редактирование книг | ✅ | ❌ |
| Создание выдачи (взять книгу) | ✅ | ✅ |
| Редактирование / удаление выдачи | ✅ | ❌ |
| Возврат книги (`return_book`) | ✅ | ❌ |

## Эндпоинты

### Аутентификация

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/v1/users/register/` | Регистрация нового пользователя |
| POST | `/api/v1/users/login/` | Получение JWT-токенов (access + refresh) |
| POST | `/api/v1/users/refresh/` | Обновление access-токена |
| GET | `/api/v1/users/me/` | Профиль текущего пользователя |

### Авторы

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/authors/` | Список авторов |
| GET | `/api/v1/authors/{id}/` | Детальная информация об авторе |
| POST | `/api/v1/authors/` | Создание автора (manager) |
| PUT/PATCH | `/api/v1/authors/{id}/` | Редактирование (manager) |
| DELETE | `/api/v1/authors/{id}/` | Удаление (manager) |

### Книги

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/books/` | Список книг (с фильтрацией) |
| GET | `/api/v1/books/{id}/` | Детальная информация о книге |
| POST | `/api/v1/books/` | Создание книги (manager) |
| PUT/PATCH | `/api/v1/books/{id}/` | Редактирование (manager) |
| DELETE | `/api/v1/books/{id}/` | Удаление (manager) |

**Параметры фильтрации книг:**

```
GET /api/v1/books/?genre=Фантастика&author=1&available=true
```

### Выдачи

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/loans/` | Список выдач |
| GET | `/api/v1/loans/{id}/` | Детальная информация о выдаче |
| POST | `/api/v1/loans/` | Создание выдачи (reader + manager) |
| PUT/PATCH | `/api/v1/loans/{id}/` | Редактирование (manager) |
| DELETE | `/api/v1/loans/{id}/` | Удаление (manager) |
| POST | `/api/v1/loans/{id}/return_book/` | Возврат книги (manager) |

### Документация

| Путь | Описание |
|------|----------|
| `/api/swagger/` | Swagger UI |
| `/api/redoc/` | ReDoc |

## Установка и запуск

### Предварительные требования

- Python 3.11+
- Poetry
- Docker Desktop (для PostgreSQL)

### 1. Клонирование репозитория

```bash
git clone <url-репозитория>
cd Library_management_API
```

### 2. Установка зависимостей

```bash
poetry install
```

### 3. Настройка переменных окружения

Создай файл `.env` в корне проекта:

```env
SECRET_KEY=django-insecure-change-me
DEBUG=True
POSTGRES_DB=library_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4. Запуск PostgreSQL

Если уже есть работающий контейнер PostgreSQL на порту 5432:

```bash
docker exec -it <имя-контейнера> psql -U postgres -c "CREATE DATABASE library_db;"
```

Если нет — подними новый:

```bash
docker run -d --name library-db -e POSTGRES_DB=library_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16-alpine
```

### 5. Миграции

```bash
poetry run python manage.py migrate
```

### 6. Создание суперпользователя

```bash
poetry run python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
poetry run python manage.py runserver
```

Сервер доступен по адресу `http://127.0.0.1:8000/`.

## Запуск через Docker Compose

```bash
docker compose up -d --build
```

Сервисы:
- `db` — PostgreSQL 16 на порту 5432
- `web` — Django-приложение на порту 8000

## Тесты

```bash
poetry run pytest --cov=users --cov=library --cov-report=term-missing
```

Покрытие: **95%** (порог — 75%).

```
18 passed, 1 warning in ~15s
```

## Примеры запросов

### Регистрация

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "reader1", "password": "pass1234"}'
```

### Логин (получение токенов)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "reader1", "password": "pass1234"}'
```

Ответ:

```json
{
  "refresh": "eyJhbGciOi...",
  "access": "eyJhbGciOi..."
}
```

### Создание книги (manager)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/books/ \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "genre": "Антиутопия", "isbn": "978-0451524935", "author": 1}'
```

### Взять книгу (reader)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/loans/ \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{"book": 1}'
```

### Возврат книги (manager)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/loans/1/return_book/ \
  -H "Authorization: Bearer <access-token>"
```

### Фильтрация книг

```bash
curl "http://127.0.0.1:8000/api/v1/books/?genre=Фантастика&available=true"
```

## Лицензия

Учебный проект. Свободное использование в образовательных целях.
