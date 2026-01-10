---
name: todo-web-app
description: Comprehensive full-stack todo web application with Next.js frontend and FastAPI backend. Use when Claude needs to work with the Phase II Hackathon II todo web app for creating Next.js 16+ web applications with App Router, implementing FastAPI REST APIs with SQLModel and Neon PostgreSQL, integrating Better Auth for authentication with JWT tokens, following spec-driven development practices, or any other Phase II todo web app tasks.
---

# Todo Web App - Phase II

## Overview

This skill provides comprehensive guidance for building a full-stack todo web application as part of Hackathon II Phase II. It includes a Next.js 16+ frontend with App Router, FastAPI backend with SQLModel and Neon PostgreSQL database, and Better Auth for user authentication using JWT tokens for secure API communication.

## Core Capabilities

### 1. Frontend Development (Next.js 16+)
- Next.js App Router architecture implementation
- Server and Client Component patterns
- Responsive UI with Tailwind CSS
- API integration and state management
- User authentication and session management

### 2. Backend Development (FastAPI)
- REST API implementation with proper endpoints
- SQLModel for database modeling and ORM
- JWT token verification and user authentication
- Database connection and session management
- API error handling and validation

### 3. Authentication Integration (Better Auth)
- Better Auth setup for Next.js frontend
- JWT token generation and validation
- User session management
- Secure API communication between frontend and backend
- User-specific data filtering

### 4. Database Management (Neon PostgreSQL)
- SQLModel database models definition
- Connection pooling and session management
- Data validation and constraints
- Migration and schema management
- Relationship handling between entities

## Project Structure

### Recommended Monorepo Structure
```
todo-web-app/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── api/
│   │   │   └── auth/
│   │   │       └── [...nextauth]/
│   │   │           └── route.ts
│   │   └── dashboard/
│   │       ├── page.tsx
│   │       └── tasks/
│   │           ├── page.tsx
│   │           └── [id]/
│   │               └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   ├── tasks/
│   │   └── auth/
│   ├── lib/
│   │   ├── api.ts
│   │   └── auth.ts
│   ├── styles/
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.js
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── auth.py
│   ├── routes/
│   │   └── tasks.py
│   ├── schemas/
│   │   └── task.py
│   ├── requirements.txt
│   └── alembic/
├── docker-compose.yml
├── CLAUDE.md
└── README.md
```

## Frontend Implementation (Next.js)

### 1. Project Setup
```bash
# Initialize Next.js project
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

### 2. Better Auth Integration
```typescript
// frontend/lib/auth.ts
import { createAuth } from "better-auth/react";
import { jwt } from "better-auth/jwt";

export const auth = createAuth({
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET || "fallback-secret",
    }),
  ],
});
```

### 3. API Client Setup
```typescript
// frontend/lib/api.ts
import { auth } from "@/lib/auth";

export const api = {
  async getTasks(userId: string) {
    const token = await auth.getClient().getSession();
    const response = await fetch(`/api/${userId}/tasks`, {
      headers: {
        'Authorization': `Bearer ${token?.accessToken}`,
      },
    });
    return response.json();
  },

  async createTask(userId: string, task: { title: string; description?: string }) {
    const token = await auth.getClient().getSession();
    const response = await fetch(`/api/${userId}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token?.accessToken}`,
      },
      body: JSON.stringify(task),
    });
    return response.json();
  },

  // Additional methods for update, delete, complete...
};
```

### 4. Task Component Example
```tsx
// frontend/components/tasks/task-list.tsx
'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Task } from '@/types/task';

export default function TaskList({ userId }: { userId: string }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTasks();
  }, [userId]);

  async function loadTasks() {
    setLoading(true);
    try {
      const data = await api.getTasks(userId);
      setTasks(data);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div>Loading tasks...</div>;

  return (
    <div className="space-y-4">
      {tasks.map(task => (
        <div key={task.id} className="p-4 border rounded-lg">
          <h3 className={task.completed ? 'line-through' : ''}>{task.title}</h3>
          {task.description && <p>{task.description}</p>}
          <p>Created: {new Date(task.createdAt).toLocaleDateString()}</p>
        </div>
      ))}
    </div>
  );
}
```

## Backend Implementation (FastAPI)

### 1. Database Models (SQLModel)
```python
# backend/models.py
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = None
```

### 2. Authentication Setup
```python
# backend/auth.py
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Header
from pydantic import BaseModel

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class TokenData(BaseModel):
    user_id: str

def verify_token(token: str = Header(...)) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return TokenData(user_id=user_id)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 3. Task Routes
```python
# backend/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.database import get_session
from backend.models import Task, TaskCreate
from backend.auth import verify_token, TokenData

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/{user_id}/tasks")
def get_tasks(user_id: str, token_data: TokenData = Depends(verify_token), session: Session = Depends(get_session)):
    if token_data.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks

@router.post("/{user_id}/tasks")
def create_task(user_id: str, task: TaskCreate, token_data: TokenData = Depends(verify_token), session: Session = Depends(get_session)):
    if token_data.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = Task(user_id=user_id, **task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

# Additional routes for update, delete, complete...
```

### 4. Main Application
```python
# backend/main.py
from fastapi import FastAPI
from backend.routes import tasks
from backend.database import engine
from backend.models import create_db_and_tables

app = FastAPI(title="Todo API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(tasks.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## API Endpoints

### REST API Specification
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for a user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get a specific task |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion status |

### Authentication Requirements
- All endpoints require valid JWT token in `Authorization: Bearer <token>` header
- Token contains user ID for authorization checks
- User can only access their own tasks

## Database Schema

### Tables
1. **users** (managed by Better Auth):
   - `id` (string, primary key)
   - `email` (string, unique)
   - `name` (string, nullable)

2. **tasks**:
   - `id` (integer, primary key)
   - `user_id` (string, foreign key → users.id)
   - `title` (string, not null)
   - `description` (text, nullable)
   - `completed` (boolean, default false)
   - `created_at` (timestamp)
   - `updated_at` (timestamp)

### Indexes
- `tasks.user_id` (for filtering by user)
- `tasks.completed` (for status filtering)

## Security Implementation

### JWT Token Flow
1. User logs in via Better Auth frontend → JWT token generated
2. Frontend includes JWT token in API request headers
3. Backend verifies JWT token signature using shared secret
4. Backend extracts user ID from token and validates access

### Shared Secret Configuration
- Set `BETTER_AUTH_SECRET` environment variable in both frontend and backend
- Both services use same secret for token signing/verification

## Development Workflow

### 1. Specification Phase
- Create detailed specs in `/specs/` directory
- Define API contracts, UI components, and database models
- Use Spec-Kit Plus for structured specifications

### 2. Implementation Phase
1. Create database models (SQLModel)
2. Implement backend API endpoints (FastAPI)
3. Create frontend components (Next.js)
4. Integrate authentication (Better Auth + JWT)
5. Connect frontend to backend API

### 3. Testing Strategy
- Unit tests for backend API endpoints
- Component tests for frontend components
- Integration tests for API authentication
- End-to-end tests for user flows

## Deployment Configuration

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:password@neon-host/db-name
BETTER_AUTH_SECRET=your-secret-key

# Frontend
NEXT_PUBLIC_BETTER_AUTH_DOMAIN=your-domain.com
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-secret-key
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Docker Compose Setup
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/todo_db
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: todo_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Resources

### references/
- `nextjs_patterns.md` - Next.js 16+ best practices and patterns
- `fastapi_guidelines.md` - FastAPI development guidelines
- `authentication_flow.md` - Better Auth and JWT implementation details
- `sqlmodel_tutorial.md` - SQLModel ORM usage and patterns
- `neon_database_setup.md` - Neon PostgreSQL configuration

### assets/
- `component_templates/` - Next.js component templates
- `api_route_templates/` - FastAPI route templates
- `database_migration_scripts/` - Alembic migration templates
- `spec_templates/` - Specification document templates
