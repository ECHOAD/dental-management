# DentalCare Pro Backend

**DentalCare Pro Backend** is a modern, scalable and modular Django REST API designed for managing the operations of a dental clinic. It supports patient management, clinical treatments, billing, inventory tracking, role-based authentication, and more. Built with clean architecture principles, this backend integrates powerful tools such as Celery, Redis, Sentry, and JWT for a robust developer and production experience.

---

## 📚 Table of Contents

- [🔧 Feature Highlights](#-feature-highlights)
- [⚙️ Configuration Guide](#-configuration-guide)
- [🚀 Quick Start Guide](#-quick-start-guide)
  - [🖥 Setting Up Locally](#-setting-up-locally)
  - [🐳 Setting Up with Docker](#-setting-up-with-docker)
- [📝 Additional Notes](#-additional-notes)

---

## 🔧 Feature Highlights

This Django API is equipped with everything you need to build and scale a real-world application:

- **🛠 Docker & Docker Compose**  
  Spin up the entire stack locally or in production with consistent environments.

- **📦 Celery with RabbitMQ and Redis** (optional) 
  Asynchronous background task support for email sending, analytics, etc.

- **🧩 Django Rest Framework (DRF)**  
  Robust RESTful APIs with full CRUD support, filtering, pagination, and more.

- **🔐 DRF Simple JWT**  
  Stateless authentication with access/refresh tokens and custom claims (e.g., role, name).

- **📑 DRF Spectacular (OpenAPI)**  
  Generate clean and customizable Swagger documentation for your API.

- **🌐 Django CORS Headers**  
  Cross-Origin Resource Sharing configured for frontend integration.

- **📊 Django Silk**  
  Profiling and performance monitoring for database queries and view logic.

- **🛡 Django Axes**  
  Protection against brute-force login attacks with lockout and logging support.

- **🗃 AWS S3 Support** *(optional)*  
  Store static and media files in scalable cloud storage.

- **📈 Sentry Integration**  
  Real-time error tracking and visibility into production failures.

- **🏗 Modular App Design**  
  Separate apps for `user`, `clinical`, `inventory`, `billing`, `notifications`, etc.

- **🚦 Soft Delete Support**  
  Patients and other entities implement soft deletion for safer data handling.

- **🔍 Dynamic Filtering & Pagination**  
  With Django Filters and global ordering/filtering exposed in OpenAPI docs.

---

## ⚙️ Configuration Guide

All environment configuration is managed via a `.env` file and works seamlessly with Docker Compose or local `uv` setups.

### 🔐 Secrets
Update the following for production security:

- `DJANGO_SECRET_KEY`
- `POSTGRES_PASSWORD`
- `RABBITMQ_DEFAULT_PASS`
- `DJANGO_ADMIN_PASSWORD`

### 🌍 Host & Ports

- API: `localhost:8010`
- RabbitMQ Dashboard: `localhost:15672`

### ⚙️ Performance
You can configure workers and threads via:

```env
WORKERS=4
THREADS=16
```

### 🌐 CORS & CSRF
Set trusted origins:

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173
```

### 💾 Database
PostgreSQL connection via:

```env
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

---

## 🚀 Quick Start Guide

### 🖥 Setting Up Locally

#### ✅ Prerequisites

- `uv`: install from [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

#### 🧩 1. Clone the Repository

```bash
git clone https://github.com/your-org/dentalcare-backend.git
cd dentalcare-backend
```

#### 📦 2. Install dependencies

```bash
uv sync --all-extras --dev
```

#### ⚙️ 3. Configuration

```bash
cp .env.example .env
```

Update any values as needed (especially secrets and ports).

#### 🗃 4. Database Setup

```bash
make migrate
```

#### 🚀 5. Run the Server

```bash
make run.server.local
```

---

### 🐳 Setting Up with Docker

#### 🧩 1. Clone the Repository

```bash
git clone https://github.com/your-org/dentalcare-backend.git
cd dentalcare-backend
```

#### ⚙️ 2. Configuration

Make sure your `.env` is properly configured.

#### 🐳 3. Run Docker Compose

```bash
docker compose up -d
```

---

## 📝 Additional Notes

- **🔐 Security**: Never commit your `.env` file or secret values to version control.
- **📈 Monitoring**: Use Sentry and Silk for real-time performance/error insights.
- **⚙️ Scalability**: Adjust Celery workers and Django threads based on production load.
- **📚 Documentation**: Visit `/schema/swagger-ui/` or `/schema/redoc/` for full API documentation.

---

## 🙌 Happy Coding!

For any issues or suggestions, feel free to open an issue or contribute to this project.
