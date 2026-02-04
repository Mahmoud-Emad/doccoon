# Doccoon Backend

Django REST API for the Doccoon markdown book editor.

## Requirements

- Python 3.14
- uv (package manager)
- PostgreSQL (production) or SQLite (development)

## Setup

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Edit .env with your values

# Run migrations
uv run python manage.py migrate

# Create superuser (optional)
uv run python manage.py createsuperuser
```

## Development

```bash
uv run python manage.py runserver
```

Runs at http://127.0.0.1:8000

## Commands

```bash
# Make migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Run tests
uv run python manage.py test

# Add a dependency
uv add <package>
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_DEBUG` | Yes | `True` or `False` |
| `ENV` | Yes | `development`, `staging`, `production` |
| `DJANGO_SECRET_KEY` | Yes | Django secret key |
| `SERVER_DOMAIN_NAME` | Yes | API domain |
| `CLIENT_DOMAIN_NAME` | Yes | Frontend domain |
| `DATABASE_*` | Prod | PostgreSQL credentials |

See `.env.example` for full list.

## API Documentation

Swagger UI available at `/swagger/` when running.

## Docker

```bash
docker build -t doccoon-backend .
docker run -d -p 8000:8000 doccoon-backend
```

## Tech Stack

- Python 3.14
- Django 6.0
- Django REST Framework
- PostgreSQL
- JWT Authentication
