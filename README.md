This project follows a separated frontend-backend architecture.

- **Frontend**: React SPA with Context API and Reducer-based state management
- **Backend**: Django API server organized by domain modules
- **Authentication**: JWT with HttpOnly access and refresh cookies
- **Database**: SQLite for local development, PostgreSQL-ready for production
- **Media Storage**: AWS S3-based storage in production
- **CI**: GitHub Actions for frontend build and backend validation
- **CD**: Git-based automatic deployment for the frontend and Dockerfile-based backend deployment
- **Backend Containerization**: Dockerfile-based container setup for production deployment

### Request Flow
1. The React client sends authenticated API requests to the Django backend.
2. Django handles authentication, business logic, and database operations.
3. Access and refresh tokens are managed through HttpOnly cookies.
4. Axios automatically retries requests after refreshing expired access tokens.
5. GitHub Actions validates the project before changes are merged into the protected `main` branch.
6. The frontend is deployed via Vercel, and the backend is deployed through a Dockerfile-based container workflow.
