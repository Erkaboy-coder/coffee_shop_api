Perfect 👍 Here’s a clean, professional, and fully-detailed **README.md** file for your **Coffee Shop API** Django + Docker + Celery + SMTP project — written in natural, developer-friendly **English** and formatted beautifully for GitHub presentation:

---

# ☕ Coffee Shop API

A **Django REST API** for user management built for a fictional Coffee Shop platform.
This project implements **user registration, authentication, email/SMS verification, role-based access**, and **asynchronous background jobs** using Celery — all wrapped in a **Dockerized, production-ready architecture**.

---

## 🚀 Features

✅ **User Registration & Verification**

* Register via email and password
* Generates a 6-digit verification code (mocked or sent via SMTP)
* Supports resending verification codes
* Automatic expiration of verification codes after 1 hour
* Unverified users deleted after 48 hours (Celery Beat)

✅ **Authentication & Authorization**

* JWT-based login (access + refresh tokens)
* Role-based permissions (User / Admin)
* `/me` endpoint for current user profile
* Admin-only endpoints for full user management

✅ **Email Integration**

* SMTP-based email sending (configurable)
* Mock console output for testing in dev mode

✅ **Asynchronous Tasks**

* Celery workers handle background jobs
* Celery Beat for periodic cleanup (delete unverified users)

✅ **Developer Experience**

* API documentation via Swagger UI (drf-yasg)
* Dockerized setup with PostgreSQL + Redis
* Easy local development (volumes + auto-reload)

---

## 🧱 Tech Stack

| Component         | Technology                       |
| ----------------- | -------------------------------- |
| Backend Framework | Django 5 + Django REST Framework |
| Auth              | JWT (SimpleJWT)                  |
| ORM               | Django ORM                       |
| Database          | PostgreSQL 16                    |
| Caching / Broker  | Redis 7                          |
| Task Queue        | Celery + Celery Beat             |
| Containerization  | Docker + Docker Compose          |
| Email             | SMTP / ConsoleBackend            |
| Documentation     | Swagger UI (drf-yasg)            |

---

## 📦 Project Structure

```
coffee_shop_api_django/
│
├── coffee_shop_api/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   ├── __init__.py
│   └── ...
│
├── users/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── permissions.py
│   └── urls.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Environment Configuration (`.env`)

Example `.env` file:

```env
# Django
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

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
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@gmail.com

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## 🐳 Docker Setup

### 1️⃣ Build and start containers

```bash
docker-compose up -d --build
```

### 2️⃣ Run migrations

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 3️⃣ Create admin user

```bash
docker-compose exec web python manage.py createsuperuser
```

### 4️⃣ Collect static files

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

Now the API will be available at:
👉 **[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)**

---

## 📡 API Endpoints Overview

| Endpoint                | Method           | Description                     | Access        |
| ----------------------- | ---------------- | ------------------------------- | ------------- |
| `/api/auth/signup`      | POST             | Register a new user             | Public        |
| `/api/auth/verify`      | POST             | Verify email with code          | Public        |
| `/api/auth/resend-code` | POST             | Resend verification code        | Public        |
| `/api/auth/login`       | POST             | JWT login                       | Public        |
| `/api/me`               | GET              | Current user info               | Authenticated |
| `/api/users`            | GET              | List all users                  | Admin         |
| `/api/users/{id}`       | GET/PATCH/DELETE | Retrieve / update / delete user | Admin         |

---

## 🧰 Example Request – Registration

**POST** `/api/auth/signup`

```json
{
  "email": "john.doe@example.com",
  "password": "strongpassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response**

```json
{
  "message": "User registered successfully. Verify your account using the provided code.",
  "email": "john.doe@example.com",
  "verification_code": "431276",
  "expires_at": "2025-10-21T15:30:00Z"
}
```

---

## ⏳ Celery Periodic Tasks

Celery Beat runs a scheduled task every 24 hours to:

* Delete users who are **not verified within 48 hours**
* Optionally resend reminders (can be extended)

---

## 🧪 Development Tips

* To see email verification codes in the console:
  check `docker-compose logs web | grep MOCK`
* To enter container shell:

  ```bash
  docker-compose exec web bash
  ```
* To monitor Celery workers:

  ```bash
  docker-compose logs worker -f
  ```

---

## 🧠 Future Improvements

* Two-Factor Authentication (2FA) via SMS
* Password reset with email token
* Admin dashboard analytics
* Docker CI/CD pipeline for production

---

## 📝 License

MIT License — Free for personal and commercial use.

---