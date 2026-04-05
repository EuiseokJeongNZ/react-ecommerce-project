# PurePro Backend | Django eCommerce API

[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://www.djangoproject.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-black?logo=githubactions)](https://github.com/features/actions)
[![Render](https://img.shields.io/badge/Backend-CD_Render-46E3B7?logo=render)](https://render.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)](https://www.docker.com/)

> Django backend API for the PurePro eCommerce project.  
> Designed to handle production-style service flows including cookie-based authentication, order snapshot storage, purchase-based review policy, automated backend testing, and containerized deployment.

---

## 🚀 Overview

This backend was built to support more than simple CRUD endpoints.
It focuses on service-side rules that are common in real commerce systems, such as authentication recovery, order consistency, purchase validation, and review reliability.

The backend covers:

- JWT authentication with HttpOnly access/refresh cookies
- product, address, profile, order, and review APIs
- order creation with shipping and product snapshot storage
- purchase-based review restriction
- domain-based module separation
- automated tests for core business rules
- Docker-based deployment to Render

---

## ✨ Core Backend Responsibilities

### Authentication
- signup, login, logout, refresh, and current-user endpoints
- JWT stored in HttpOnly cookies
- access token recovery through backend auth utility

### Product & Profile APIs
- product list and detail APIs
- profile data retrieval for authenticated user

### Address APIs
- create, update, delete, and default-address handling
- ownership-based access control for user addresses

### Order APIs
- order creation with request validation
- address ownership validation before order creation
- duplicate product validation inside order items
- stock validation before confirming an order
- shipping fee calculation based on subtotal
- user-specific order history retrieval
- shipping and product snapshot storage at order time

### Review APIs
- create, update, delete, and list review endpoints
- only purchased users can create reviews
- one review per user per product
- average rating and review count are recalculated automatically

---

## 🧠 Architecture Decisions

### Cookie-based JWT Authentication
The backend uses HttpOnly cookies for access and refresh tokens to support a more production-oriented authentication flow and reduce direct exposure of tokens in client-side JavaScript.

### Order Snapshot Design
At the time of order creation, shipping information and product information are stored as snapshot values. This ensures historical order data remains stable even if product information changes later.

### Purchase-based Review Policy
Review creation is restricted to users with eligible purchase history. This prevents arbitrary review creation and makes the review system more reliable.

### Domain-based Backend Structure
The backend is organized by domain modules such as auth, products, addresses, orders, profile, and reviews. This improves readability and makes feature-specific maintenance easier.

---

## 🛠️ Technologies Used

- Django
- Django ORM
- Django REST Framework
- Simple JWT
- Gunicorn
- Whitenoise
- django-storages
- boto3
- Docker
- GitHub Actions
- Render

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
│   ├── utils/
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

Authentication is implemented using JWT stored in HttpOnly cookies.

### Flow
1. User logs in
2. Backend issues access and refresh tokens
3. Tokens are stored in HttpOnly cookies
4. Frontend sends authenticated requests with `withCredentials: true`
5. When the access token expires, frontend requests `/api/auth/refresh/`
6. Backend validates refresh token and reissues a new access token

This approach is closer to a deployable service flow than storing tokens directly in local storage.

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
- shipping fee calculation
- stock validation

### Reviews
- create review
- update review
- delete review
- get product reviews
- get my reviews
- purchase-based review restriction

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
- review model updates **avg_rating** and **review_count** automatically
- backend is organized by **domain-based modules**

---

## 🧪 Testing

This backend includes tests for core business logic, model behavior, and validation utilities.

### Covered areas
- auth views
- order views
- review views
- review model
- validator utils
- auth utility

### What is tested
- signup, login, logout, refresh flow
- access/refresh cookie handling
- unauthorized access blocking
- order validation and stock updates
- shipping fee calculation
- purchase-based review creation
- duplicate review prevention
- review rating aggregation and deletion behavior
- validator boundary cases
- current-user resolution from access token

### Example command
```bash
python manage.py test
```

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

## 🐳 Docker

This backend includes a Dockerfile for container-based deployment.

### Build image

```bash
docker build -t purepro-backend .
```

### Run container

```bash
docker run -p 8000:8000 purepro-backend
```

---

## 🧪 CI Workflow

This backend uses GitHub Actions to verify backend quality before deployment.

### Current backend checks
- dependency install
- migration consistency check
- Django system check
- automated backend test execution

### CI summary
- **CI**: GitHub Actions
- validates backend project health and core service logic before merge or deployment

---

## 🚢 CD / Deployment

This backend uses continuous deployment to Render.

### Backend CD
- Render for Django backend hosting
- deployed using a Dockerfile-based containerized setup
- production frontend connects to the deployed backend API

### Deployment Summary
- **CI**: GitHub Actions
- **CD**: Render
- **Containerization**: Docker

---

## 📌 Future Improvements

- standardize backend error response format
- separate settings by environment more clearly
- improve serializer and validation structure
- add admin dashboard and management tools
- optimize filtering, sorting, and pagination
- improve logging and monitoring
- add API documentation

---

## 👨‍💻 Author

**Euiseok Jeong**  
- [LinkedIn](https://www.linkedin.com/in/euiseok-jeong-965b9b310)
