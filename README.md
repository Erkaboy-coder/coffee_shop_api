---

# ☕ Coffee Shop API

A **Django REST API** for user management built for a fictional Coffee Shop platform.
It provides **user registration, authentication, email verification, role-based access**, and **asynchronous background jobs** using Celery — all within a **Dockerized, production-ready architecture**.

---

## 🚀 Features

✅ **User Registration & Verification**

* Register via email and password
* Generates a 6-digit verification code (sent via SMTP)
* Supports resending verification codes
* Codes expire automatically after 1 hour
* Unverified users are deleted after 48 hours (Celery Beat)

✅ **Authentication & Authorization**

* JWT-based login (access + refresh tokens)
* Role-based permissions (User / Admin)
* `/me` endpoint for current user info
* Admin-only endpoints for full user management

✅ **Email Integration**

* SMTP-based email sending via Gmail App Password
* Configurable via environment variables

✅ **Asynchronous Background Jobs**

* Celery workers handle email sending in the background
* Celery Beat performs scheduled cleanup tasks

✅ **Caching & Performance**

* Redis caching for user list endpoint
* Automatic cache invalidation on user create/update/delete

✅ **Developer Experience**

* API documentation with Swagger UI (`drf-yasg`)
* Dockerized setup with PostgreSQL + Redis + Celery
* Auto-reload in development using volumes

---

## 🧱 Tech Stack

| Component         | Technology                       |
| ----------------- | -------------------------------- |
| Backend Framework | Django 5 + Django REST Framework |
| Authentication    | JWT (SimpleJWT)                  |
| ORM               | Django ORM                       |
| Database          | PostgreSQL 16                    |
| Caching / Broker  | Redis 7                          |
| Task Queue        | Celery + Celery Beat             |
| Containerization  | Docker + Docker Compose          |
| Email             | SMTP (Gmail App Password)        |
| Documentation     | Swagger UI (drf-yasg)            |

---

## 📂 Project Structure

```
coffee_shop_api_django/
│
├── coffee_shop_api/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── __init__.py
│
├── users/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── permissions.py
│   ├── signals.py
│   └── urls.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Environment Variables (`.env`)

```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=coffee_db
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Email (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

---

## 🐳 Docker Setup

### 1️⃣ Build and start all containers

```bash
docker-compose up -d --build
```

### 2️⃣ Apply migrations

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 3️⃣ Create a superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 4️⃣ Collect static files

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 🌐 Access the API

Once the containers are running, open:
👉 **[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)**
or visit:
👉 **[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)**

---

## 📡 API Endpoints

| Endpoint                | Method           | Description                     | Access        |
| ----------------------- | ---------------- | ------------------------------- | ------------- |
| `/api/auth/signup`      | POST             | Register a new user             | Public        |
| `/api/auth/verify`      | POST             | Verify email with code          | Public        |
| `/api/auth/resend-code` | POST             | Resend verification code        | Public        |
| `/api/auth/login`       | POST             | JWT login                       | Public        |
| `/api/me`               | GET              | Current user info               | Authenticated |
| `/api/users`            | GET              | List all users (cached)         | Admin         |
| `/api/users/{id}`       | GET/PATCH/DELETE | Retrieve / update / delete user | Admin         |

---

## 🧩 Example – Registration Flow

**POST** `/api/auth/signup`

```json
{
  "email": "john.doe@example.com",
  "password": "StrongPass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response**

```json
{
  "message": "User registered successfully. Verification code sent to your email.",
  "email": "john.doe@example.com",
  "expires_at": "2025-10-21T15:30:00Z"
}
```

---

## ⏰ Celery Periodic Tasks

Celery Beat automatically runs scheduled background jobs:

* Deletes **unverified users** older than 48 hours
* Can be extended for future recurring jobs (e.g., reminders, analytics updates)

---

## ⚡ Redis Caching Behavior

* `UserListView` uses Redis for caching the user list.
* Cache expires after 5 minutes automatically.
* Whenever a user is created, updated, or deleted → cache is cleared via Django signals.

You can verify Redis caching:

```bash
docker-compose exec web python manage.py shell
```

```python
from django.core.cache import cache
cache.set('hello', 'redis_test')
print(cache.get('hello'))
```

---

## 🧠 Development Tips

* View logs for Django:

  ```bash
  docker-compose logs web -f
  ```
* View logs for Celery workers:

  ```bash
  docker-compose logs worker -f
  ```
* Enter the web container:

  ```bash
  docker-compose exec web bash
  ```

---

## 🔮 Future Improvements

* Two-Factor Authentication (2FA) via SMS
* Password reset with email link
* Admin dashboard with analytics
* CI/CD pipeline for production deployment

---

## 📝 License

MIT License — Free to use and modify.

---
