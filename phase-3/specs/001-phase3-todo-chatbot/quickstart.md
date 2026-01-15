# Quickstart Guide: Todo AI Chatbot

## Prerequisites

- Python 3.13+
- Node.js 18+
- UV package manager
- Git
- Neon Serverless PostgreSQL account
- OpenAI API key

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

#### Install Dependencies
```bash
cd backend
uv sync --all-extras
```

#### Environment Configuration
Create a `.env` file in the `backend` directory:
```env
DATABASE_URL=postgresql://user:password@localhost/todo_db
BETTER_AUTH_SECRET=your_auth_secret_key
BETTER_AUTH_URL=http://localhost:3000
OPENAI_API_KEY=your_openai_api_key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

#### Database Setup
Run database migrations:
```bash
uv run python -m alembic upgrade head
```

#### Start Backend Server
```bash
uv run uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
# or
pnpm install
```

#### Environment Configuration
Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your_auth_secret_key
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_openai_domain_key
```

#### Start Frontend Development Server
```bash
npm run dev
# or
pnpm dev
```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

## Architecture Overview

### Components
- **Frontend**: OpenAI ChatKit UI utilizing ChatKit widgets for natural language interaction and conversation history management
- **Backend**: FastAPI server with pluggable AI agent architecture (currently OpenAI Agents SDK, extensible to other providers) and MCP server
- **Database**: Neon PostgreSQL storing tasks, conversations, and messages for conversation history preservation
- **Authentication**: Better Auth with JWT tokens

### Data Flow
1. User sends message through ChatKit UI widgets (ensuring conversation history is maintained)
2. Frontend attaches JWT token and sends to backend
3. Backend validates JWT and loads conversation history from database
4. Backend stores user message in database
5. Backend runs AI agent with MCP tools (through pluggable agent architecture)
6. Agent selects appropriate MCP tool based on intent
7. MCP tool performs database operation with user validation
8. Backend stores assistant response in database
9. Response returned to frontend with preserved conversation history

### ChatKit Widgets for Conversation History
- The frontend must utilize ChatKit widgets to ensure conversation history is properly maintained
- All conversation history must be persisted in the database for reconstruction
- ChatKit widgets will load conversation history from backend to maintain context

### Alternative AI Provider Configuration
**Note**: The architecture supports pluggable AI services to allow integration with different LLM providers:
- Current implementation uses OpenAI Agents SDK
- Future implementations could integrate Google Gemini or other providers through an adapter layer
- The MCP tool architecture remains consistent regardless of the underlying AI provider

## Key Endpoints

### Backend
- `POST /api/{user_id}/chat` - Chat endpoint for conversation
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

### MCP Tools
- `add_task` - Create new task via AI agent
- `list_tasks` - Retrieve tasks via AI agent
- `update_task` - Update task via AI agent
- `delete_task` - Delete task via AI agent
- `complete_task` - Toggle completion via AI agent

## Development Workflow

### Adding New Features
1. Update the specification in `specs/`
2. Run `/sp.plan` to update the implementation plan
3. Create tasks using `/sp.tasks`
4. Implement code following the tasks
5. Write tests for new functionality
6. Run tests to ensure everything works

### Running Tests
```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests
cd frontend
npm test
```

## Troubleshooting

### Common Issues
- **JWT Validation Errors**: Ensure `BETTER_AUTH_SECRET` matches between frontend and backend
- **Database Connection Issues**: Verify `DATABASE_URL` is correct
- **MCP Tools Not Working**: Check that MCP server is running and properly configured
- **CORS Errors**: Ensure `ALLOWED_ORIGINS` includes your frontend URL

### Environment Variables
Make sure all required environment variables are set in both frontend and backend:
- Backend: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `OPENAI_API_KEY`
- Frontend: `NEXT_PUBLIC_BETTER_AUTH_URL`, `NEXT_PUBLIC_API_BASE_URL`

## Next Steps

1. Explore the API documentation at `/docs` when running the backend
2. Review the MCP tool specifications in the contracts directory
3. Check out the existing tests for examples of how to test your code
4. Look at the data model documentation for database schema details