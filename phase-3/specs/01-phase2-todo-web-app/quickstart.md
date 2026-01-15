# Quickstart Guide: Phase-2 Todo Web Application

**Date**: 2026-01-03
**Feature**: Phase-2 Todo Web Application
**Branch**: 01-phase2-todo-web-app

## Overview

This guide provides a quick setup and development workflow for the Phase-2 Todo Web Application. This application is a full-stack web application with Next.js frontend, FastAPI backend, SQLModel ORM, and Neon Serverless PostgreSQL database.

## Prerequisites

- Node.js 18+ and npm/pnpm
- Python 3.13+
- UV package manager
- Git
- A Neon Serverless PostgreSQL account
- Better Auth account (or self-hosted auth solution)

## Environment Setup

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Setup Python Environment

```bash
# Install UV if not already installed
pip install uv

# Navigate to backend directory
cd backend

# Install Python dependencies
uv sync --all-extras
# or if using requirements.txt
uv pip install -r requirements.txt
```

### 3. Setup Frontend Environment

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
# or
pnpm install
```

### 4. Environment Configuration

#### Backend Configuration

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL="your_neon_database_connection_string"
BETTER_AUTH_SECRET="your_auth_secret_key"
BETTER_AUTH_URL="http://localhost:3000"  # Frontend URL
```

#### Frontend Configuration

Create a `.env.local` file in the `frontend` directory:

```env
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_BETTER_AUTH_SECRET="your_auth_secret_key"
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api"
```

## Development Workflow

### 1. Starting the Backend (FastAPI)

```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`.

### 2. Starting the Frontend (Next.js)

```bash
cd frontend
npm run dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000`.

### 3. Running Tests

#### Backend Tests

```bash
cd backend
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=.

# Run specific test file
uv run pytest tests/test_tasks.py
```

#### Frontend Tests

```bash
cd frontend
# Run all tests
npm test
# or
pnpm test

# Run tests in watch mode
npm run test:watch
# or
pnpm run test:watch
```

## API Endpoints

The backend provides the following REST API endpoints:

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Task Management Endpoints
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Database Migrations

### Running Migrations

```bash
cd backend
uv run python -m alembic upgrade head
```

### Creating New Migrations

```bash
cd backend
uv run python -m alembic revision --autogenerate -m "description of migration"
uv run python -m alembic upgrade head
```

## Running in Production

### Backend Production Build

```bash
cd backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Production Build

```bash
cd frontend
npm run build
npm start
# orJ
pnpm build
pnpm start
```

## Docker Deployment (Optional)

### Building Docker Images

```bash
# Build backend image
docker build -t todo-backend -f backend/Dockerfile .

# Build frontend image
docker build -t todo-frontend -f frontend/Dockerfile .
```

### Running with Docker Compose

```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify `DATABASE_URL` is correctly set in backend `.env`
   - Ensure Neon database is active and accessible

2. **Authentication Issues**
   - Check that `BETTER_AUTH_SECRET` matches between frontend and backend
   - Verify JWT token configuration

3. **Frontend-Backend Communication**
   - Ensure API endpoints are correctly configured
   - Check CORS settings in FastAPI backend

### Useful Commands

```bash
# Check backend API status
curl http://localhost:8000/health

# Check frontend build
cd frontend && npm run build && npm start
```

## Next Steps

1. Implement the basic task CRUD functionality
2. Add authentication flows
3. Implement responsive UI components
4. Add comprehensive tests
5. Deploy to Vercel (frontend) and preferred backend hosting