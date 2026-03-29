# PurePro | Full Stack eCommerce Web App

[![React](https://img.shields.io/badge/React-18.2-blue?logo=react)](https://react.dev/)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://www.djangoproject.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-black?logo=githubactions)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Backend-Docker-blue?logo=docker)](https://www.docker.com/)

> 🛒 Full stack protein store eCommerce web application built with **React** and **Django**.  
> Includes authentication, product browsing, cart, address management, orders, reviews, CI workflow, and Dockerfile-based backend deployment.

---

## 🚀 Overview

PurePro is a full stack eCommerce project designed to simulate a modern online store experience.

The project is built with:

- **Frontend**: React SPA with Context API and Reducer-based state management
- **Backend**: Django API server organised by domain modules
- **Authentication**: JWT with HttpOnly access/refresh cookies
- **Database**: SQLite for local development, PostgreSQL-ready for production
- **Deployment**: Vercel for frontend, Dockerfile-based backend deployment
- **CI**: GitHub Actions for frontend build and backend validation

---

## ✨ Core Features

- 🔐 User authentication with HttpOnly cookie-based JWT flow
- 🛍️ Product list and product detail pages
- 🛒 Cart management
- 📦 Address management
- 🧾 Order creation and order history
- ⭐ Review creation, update, and deletion
- ✅ Purchase-based review policy
- 🎯 Product filtering and sorting
- 🌙 Responsive dark-themed UI
- 🔄 Access token refresh with Axios interceptor
- 🐳 Dockerfile-based backend containerization
- ⚙️ GitHub Actions CI workflow

---

## 🛠️ Tech Stack

### Frontend
- **React**
- **React Router**
- **Context API + Reducer**
- **Axios**
- **SASS**
- **Swiper**

### Backend
- **Django**
- **Django ORM**
- **Django REST Framework**
- **Simple JWT**
- **Gunicorn**
- **Whitenoise**
- **django-storages / boto3**

### DevOps / Deployment
- **GitHub Actions**
- **Docker**
- **Vercel**
- **Render-ready deployment structure**

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    DEV[Developer] -->|Code / Commit / Push| GH[GitHub Repository]
    GH -->|Pull Request / Push Trigger| CI[GitHub Actions CI<br/>Frontend Build · Backend Check]
    CI -->|Checks Passed| MAIN[Protected main Branch]

    MAIN -->|Auto Deploy| VERCEL[Vercel<br/>Frontend Hosting]
    MAIN -->|Auto Deploy| RENDER[Render<br/>Backend Hosting]

    GH -.contains.-> DOCKER[Dockerfile<br/>Backend Container Definition]
    DOCKER -.used by.-> RENDER

    U[User Browser] -->|Load Web App| VERCEL
    VERCEL --> FE[React SPA<br/>Runs in Browser]

    FE --> STATE[Context / Reducer State<br/>Auth · Cart · Filters]
    FE --> AXIOS[Axios Instance<br/>withCredentials · 401 Refresh Interceptor]

    AXIOS -->|HTTPS API Requests| RENDER
    RENDER --> BE[Django API Server<br/>Backend]

    BE --> AUTH[JWT Authentication<br/>HttpOnly access / refresh cookies]
    BE --> API[Domain APIs<br/>Auth · Products · Address · Orders · Reviews]
    BE --> ORM[Django ORM]

    ORM --> DB[(SQLite Local Dev<br/>PostgreSQL-ready Production)]
    BE --> MEDIA[Media Storage<br/>AWS S3 in Production]

    BE -->|Set access / refresh cookies| U
    U -->|Auto-send cookies| AXIOS
    AXIOS -->|POST /api/auth/refresh/| RENDER
```

---

## 📁 Project Structure

```bash
react-ecommerce-project/
├── client/                  # React frontend
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── data/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── routes/
│   ├── package.json
│   └── README.md
│
├── server/                  # Django backend
│   ├── config/
│   ├── shop/
│   │   ├── migrations/
│   │   ├── models/
│   │   ├── views/
│   │   └── urls.py
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── erd.mmd
└── systemArchitecture.mmd
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/react-ecommerce-project.git
cd react-ecommerce-project
```

### 2. Frontend setup

```bash
cd client
npm install
npm start
```

Frontend runs on:

```bash
http://localhost:3000
```

### 3. Backend setup

```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

## 🔐 Environment Variables

Create environment files for frontend and backend as needed.

### Example frontend
```env
REACT_APP_API_URL=http://127.0.0.1:8000
```

### Example backend
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

This project includes a GitHub Actions workflow for continuous integration.

### Current checks
- Frontend build
- Backend validation

### CI flow
1. Code is pushed to GitHub
2. GitHub Actions runs frontend and backend checks
3. Protected `main` branch requires checks before merge

---

## 🚢 Deployment

### Frontend
- **Vercel**

### Backend
- **Dockerfile-based deployment**
- **Render-ready deployment structure**

---

## 📌 Roadmap

- Improve frontend lint compliance without CI workaround
- Add test coverage for core backend flows
- Add backend-side filtering, sorting, and pagination
- Improve admin management features
- Refine cart persistence
- Enhance deployment automation

---

## 👨‍💻 Author

**Euiseok Jeong**  
- [LinkedIn](https://www.linkedin.com/in/euiseok-jeong-965b9b310)

---

## 📜 License

This project is for portfolio and educational purposes.
