# Research Summary: Todo AI Chatbot

## Architecture Overview

The Todo AI Chatbot implements a stateless conversational interface using OpenAI's ecosystem. The system consists of:
- Frontend: OpenAI ChatKit UI for natural language interaction
- Backend: FastAPI server orchestrating conversation flow
- AI Agent: OpenAI Agents SDK processing user intent
- MCP Server: Official MCP SDK exposing task operations as tools
- Database: Neon PostgreSQL storing tasks, conversations, and messages

## Key Technical Decisions

### 1. MCP Tool Design
**Decision**: Implement 5 core MCP tools for task operations
- add_task: Creates new tasks with title/description
- list_tasks: Retrieves tasks with optional filtering
- update_task: Modifies existing task properties
- delete_task: Removes tasks from user's list
- complete_task: Toggles completion status

**Rationale**: These align with the basic todo operations specified in the requirements and provide a clean interface for the AI agent to interact with the system.

**Alternatives considered**:
- Single generic "task_operation" tool: Would require more complex parameter validation
- REST API endpoints directly: Would bypass the MCP architecture requirement

### 2. Authentication Flow
**Decision**: JWT-based authentication with Better Auth
- Frontend handles user authentication via Better Auth
- JWT tokens passed in Authorization header with each request
- Backend validates JWT and enforces user_id matching for all operations

**Rationale**: Maintains separation of concerns while ensuring security. Better Auth provides a robust authentication solution while the backend enforces authorization.

**Alternatives considered**:
- Session-based authentication: Would add complexity to stateless design
- OAuth tokens: Overkill for this application scope

### 3. Conversation State Management
**Decision**: Database-backed state with stateless server
- All conversation history stored in database
- Server reconstructs context from database for each request
- No in-memory conversation state maintained

**Rationale**: Enables horizontal scalability while preserving conversation context across server restarts.

**Alternatives considered**:
- In-memory state: Would complicate horizontal scaling
- Client-side storage: Would expose sensitive data and complicate consistency

### 4. AI Agent Integration
**Decision**: Pluggable AI agent architecture with MCP tools
- FastAPI backend orchestrates agent execution through an abstraction layer
- MCP tools provide standardized interface for database operations
- Agent uses tools based on natural language intent recognition
- Architecture supports multiple AI providers (initially OpenAI, extensible to others like Google Gemini)

**Rationale**: Aligns with Phase III requirements for MCP architecture while maintaining flexibility for different AI providers.

**Alternatives considered**:
- Direct API calls from agent: Would violate MCP architecture requirement
- Custom NLP solution: Would require significant development effort
- Tightly coupled to single provider: Would limit flexibility for future changes

### 5. Database Schema Design
**Decision**: Three main entities with user_id scoping
- Task: user_id, title, description, completion status, timestamps
- Conversation: user_id, timestamps
- Message: user_id, conversation_id, role, content, timestamps

**Rationale**: Provides clear separation of concerns while ensuring user data isolation and conversation tracking.

**Alternatives considered**:
- Single unified table: Would complicate queries and data relationships
- No user scoping: Would violate security requirements

## Technology Stack Rationale

### Backend Technologies
- **FastAPI**: Provides excellent performance, automatic API documentation, and Pydantic validation
- **SQLModel**: Combines SQLAlchemy and Pydantic for type-safe database operations
- **OpenAI Agents SDK**: Official solution for creating AI agents with tool use
- **Official MCP SDK**: Required for MCP tool implementation

### Frontend Technologies
- **OpenAI ChatKit**: Provides pre-built chat interface optimized for AI interactions
- **Next.js 16+**: Modern React framework with App Router for structured application
- **TypeScript 5+**: Type safety for frontend code

### Infrastructure
- **Neon Serverless PostgreSQL**: Scales automatically and provides familiar SQL interface
- **Better Auth**: Robust authentication solution with JWT support

## Implementation Patterns

### Stateless Request Flow
1. Receive user message
2. Load conversation history from database
3. Store user message in database
4. Run agent with MCP tools
5. Agent executes appropriate tools
6. Store assistant response in database
7. Return response to client

### MCP Tool Security
- Each tool validates JWT token
- Tools enforce user_id matching for all operations
- No direct database access outside of MCP tools

### Error Handling Strategy
- 401 for missing/invalid JWT
- 403 for cross-user access attempts
- 404 for missing tasks
- 422 for validation errors

## Security Considerations

### Input Validation
- All user inputs validated through Pydantic models
- MCP tools validate inputs before database operations
- JWT tokens validated for all requests

### Data Isolation
- All queries filtered by user_id
- MCP tools enforce user ownership for operations
- No cross-user data access possible

### Prompt Injection Protection
- Agent will not follow instructions to reveal secrets
- Backend will not place secrets in model messages
- Untrusted user input is properly sanitized