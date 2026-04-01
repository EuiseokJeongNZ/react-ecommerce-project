# PurePro Backend | Django eCommerce API

[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://www.djangoproject.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-black?logo=githubactions)](https://github.com/features/actions)
[![Render](https://img.shields.io/badge/Deployment-Render-46E3B7?logo=render)](https://render.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)](https://www.docker.com/)

> ⚙️ Backend API for the PurePro eCommerce project built with **Django**.  
> Handles authentication, products, addresses, orders, profile, and reviews, with **GitHub Actions CI** and **Docker-based deployment on Render**.

---

## 🚀 Overview

This backend provides the core business logic and API layer for the PurePro eCommerce application.

It supports:

- user authentication
- product data handling
- address management
- order processing
- review management
- JWT-based cookie authentication
- GitHub Actions CI for backend validation
- Docker-based backend deployment on Render

---

## ✨ Core Features

- 🔐 JWT authentication with HttpOnly access and refresh cookies
- 👤 User profile handling
- 🛍️ Product listing and product detail APIs
- 🏠 Address CRUD
- 📦 Order creation and order history
- ⭐ Review create / update / delete
- ✅ Purchase-based review permission logic
- 🐳 Dockerfile-based containerized deployment
- ☁️ Production-ready media storage structure
- ⚙️ GitHub Actions CI validation
- 🚀 Render deployment for production backend hosting

---

## 🛠️ Technologies Used

- **Django**
- **Django ORM**
- **Django REST Framework**
- **Simple JWT**
- **Gunicorn**
- **Whitenoise**
- **django-storages**
- **boto3**

### DevOps / Deployment
- **GitHub Actions** (CI)
- **Docker** (containerized backend deployment)
- **Render** (production backend hosting)

---

## 📁 Backend Structure

```bash
server/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── shop/
│   ├── migrations/
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── address.py
│   │   ├── order.py
│   │   └── review.py
│   │
│   ├── views/
│   │   ├── auth_views.py
│   │   ├── product_views.py
│   │   ├── address_views.py
│   │   ├── profile_views.py
│   │   ├── order_views.py
│   │   └── review_views.py
│   │
│   ├── admin.py
│   ├── urls.py
│   └── apps.py
│
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## 🔑 Authentication Flow

Authentication is implemented using JWT stored in **HttpOnly cookies**.

### Flow
1. User logs in
2. Backend issues:
   - access token
   - refresh token
3. Tokens are stored in HttpOnly cookies
4. Frontend sends requests with `withCredentials: true`
5. When access expires, frontend requests `/api/auth/refresh/`

This approach improves security compared to storing tokens in local storage.

---

## 📦 Domain Modules

### Auth
- signup
- login
- logout
- token refresh
- current user info

### Products
- product list
- product detail
- product images

### Address
- create address
- update address
- delete address
- set default address

### Orders
- create order
- get order history
- order item snapshot handling

### Reviews
- create review
- update review
- delete review
- restrict reviews to eligible users

### Profile
- current user profile data

---

## 🗃️ Data Model Highlights

Main entities:

- **User**
- **Product**
- **ProductImage**
- **Address**
- **Order**
- **OrderItem**
- **Review**

### Key design points
- order data stores **snapshot values**
- review access is controlled by **purchase history**
- media storage is prepared for **production storage services**
- backend is organized by **domain-based modules**

---

## ⚙️ Local Development

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Run development server

```bash
python manage.py runserver
```

Backend default local URL:

```bash
http://127.0.0.1:8000
```

---

## 🔐 Environment Variables

Example `.env` values:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
DATABASE_URL=sqlite:///db.sqlite3
```

Optional production-related values:

```env
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=your-region
```

---

## 🧪 CI Workflow

This backend is connected to GitHub Actions for continuous integration.

### Current backend checks
- dependency install
- migration consistency check
- Django system check
- test command execution

### CI flow
1. Code is pushed to GitHub
2. GitHub Actions runs backend validation steps
3. Changes are merged only after required checks pass

---

## 🚢 Deployment

This backend is deployed as a containerized Django service.

### Production Hosting
- **Render** for backend hosting
- **Dockerfile-based deployment** for consistent build and runtime setup

### Deployment Summary
- **CI**: GitHub Actions
- **Deployment**: Render
- **Containerization**: Docker

---

## 📌 Future Improvements

- add more automated tests
- separate settings by environment
- improve serializer / validation structure
- enhance admin features
- optimize product filtering and pagination
- improve production deployment configuration

---

## 👨‍💻 Author

**Euiseok Jeong**  
- [LinkedIn](https://www.linkedin.com/in/euiseok-jeong-965b9b310)
