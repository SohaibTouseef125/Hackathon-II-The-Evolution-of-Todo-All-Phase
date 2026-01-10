# Phase-2 Todo Web Application

A full-stack web application that transforms the Phase I in-memory Python console Todo application into a modern multi-user web application with persistent storage using Next.js (frontend), FastAPI (backend), SQLModel (ORM), and Neon Serverless PostgreSQL (database).

## Features

- **User Authentication**: Secure signup and login with JWT token validation
- **Task Management**: Create, read, update, delete, and mark tasks as complete
- **Multi-User Support**: Each user sees only their own tasks
- **Responsive UI**: Works on desktop and mobile devices
- **RESTful API**: Well-designed endpoints with proper error handling

## Tech Stack

### Frontend
- Next.js 16+ with App Router
- React 19
- TypeScript 5+
- Tailwind CSS for styling
- Client-side authentication with JWT tokens

### Backend
- FastAPI for the web framework
- Python 3.13+
- SQLModel for ORM operations
- Neon Serverless PostgreSQL for database
- JWT token validation for authentication
- Pydantic for request/response validation

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLModel database models
├── db.py                # Database connection utilities
├── auth.py              # Authentication utilities
├── routes/
│   ├── __init__.py
│   ├── tasks.py         # Task CRUD API endpoints
│   └── auth.py          # Authentication API endpoints
├── schemas/             # Pydantic models for request/response validation
├── services/            # Business logic services
├── middleware/          # Authentication and authorization middleware
├── utils/               # Utility functions
├── tests/               # Test files
└── requirements.txt     # Python dependencies

frontend/
├── package.json         # Node.js dependencies
├── next.config.js       # Next.js configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
├── public/              # Static assets
├── src/
│   ├── app/             # Next.js App Router pages
│   ├── components/      # Reusable UI components
│   ├── lib/             # Utility functions and API client
│   ├── types/           # TypeScript type definitions
│   ├── styles/          # Global styles
│   └── hooks/           # Custom React hooks
└── __tests__/           # Alternative test location
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.13+
- UV package manager
- Git
- A Neon Serverless PostgreSQL account

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   uv sync --all-extras
   # or if using requirements.txt
   uv pip install -r requirements.txt
   ```

3. Create a `.env` file in the `backend` directory:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/todo_db
   BETTER_AUTH_SECRET=your_auth_secret_key
   BETTER_AUTH_URL=http://localhost:3000
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
   ```

4. Start the backend server:
   ```bash
   uv run uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   # or
   pnpm install
   ```

3. Create a `.env.local` file in the `frontend` directory:
   ```env
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   NEXT_PUBLIC_BETTER_AUTH_SECRET=your_auth_secret_key
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

## API Endpoints

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
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Testing

### Backend Tests
```bash
cd backend
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=.

# Run specific test file
uv run pytest tests/test_tasks.py
```

### Frontend Tests
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

## Security Features

- JWT token validation on all protected endpoints
- User data isolation - users can only access their own tasks
- Input validation using Pydantic models
- SQL injection prevention through ORM usage
- Proper session management

## Data Model

### User
- id: Unique identifier (managed by auth system)
- email: User's email address (unique)
- name: User's display name (optional)
- created_at: Timestamp when user account was created
- updated_at: Timestamp when user account was last updated

### Task
- id: Primary key, auto-incremented
- user_id: Foreign key linking to User (required)
- title: Task title (required, 1-200 characters)
- description: Task description (optional, max 1000 characters)
- completed: Task completion status (default: false)
- created_at: Timestamp when task was created
- updated_at: Timestamp when task was last updated

## Environment Variables

### Backend
- `DATABASE_URL`: Connection string for the PostgreSQL database
- `BETTER_AUTH_SECRET`: Secret key for JWT token generation
- `BETTER_AUTH_URL`: Frontend URL for auth redirects
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for the auth system

## Development Workflow

1. Set up both frontend and backend environments
2. Start both servers (backend on port 8000, frontend on port 3000)
3. Make changes to either frontend or backend as needed
4. Test functionality by creating accounts and managing tasks
5. Run tests to ensure functionality remains intact
6. Commit changes with descriptive commit messages

## Deployment

### Frontend
The frontend is designed to be deployed to Vercel:
```bash
npm run build
npm start
```

### Backend
The backend can be self-hosted:
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```