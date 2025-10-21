# Coffee Shop API — User Management (Django + DRF)

Production-ready user module with registration, JWT auth (access/refresh), email verification (mock), roles (User/Admin), RBAC, and automatic cleanup of unverified accounts via Celery.

## Stack
- Django 5, Django REST Framework
- JWT with `djangorestframework-simplejwt`
- PostgreSQL (or SQLite for quick start)
- Celery + Redis (periodic cleanup task)
- Swagger/Redoc via `drf-yasg`
- Docker + docker-compose
- English comments & summaries as required

## Run (Docker)
```bash
cp .env.example .env
docker-compose up --build
# API:        http://localhost:8000/api/
# Swagger:    http://localhost:8000/swagger/
# Redoc:      http://localhost:8000/redoc/
```
Create superuser (optional):
```bash
docker-compose exec web python manage.py createsuperuser --email admin@example.com
```

## Endpoints
- `POST /api/auth/signup/` – register (prints verification code to console)
- `POST /api/auth/login/` – get access/refresh tokens
- `POST /api/auth/verify/` – confirm verification with code
- `POST /api/auth/refresh/` – refresh tokens
- `GET /api/me/` – current user (auth required)
- `GET /api/users/` – list users (admin)
- `GET|PATCH|DELETE /api/users/{id}/` – admin user management

## Cleanup job
Celery beat runs daily at 02:00 UTC and deletes users unverified after 2 days.

## Notes / Simplifications
- Verification is mocked via console print. Replace with an email/SMS provider (e.g., SendGrid/Twilio).
- Admin permissions are checked by custom `IsAdminRole` (role='admin' or is_staff=True).
"# coffee_shop_api" 
