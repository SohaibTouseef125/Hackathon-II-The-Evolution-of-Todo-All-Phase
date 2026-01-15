# Implementation Plan: Todo AI Chatbot

**Branch**: `001-phase3-todo-chatbot` | **Date**: 2026-01-12 | **Spec**: [specs/001-phase3-todo-chatbot/spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase3-todo-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered chatbot for todo management using OpenAI ChatKit UI, FastAPI chat endpoint, OpenAI Agents SDK, Official MCP SDK, and Neon PostgreSQL. The system provides natural language interaction for all basic todo operations (add, list, update, delete, complete) while maintaining stateless server architecture with database-backed conversation persistence.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5+ (frontend), Next.js 16+ (App Router)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon Serverless PostgreSQL, Better Auth, OpenAI ChatKit
**Storage**: Neon Serverless PostgreSQL database with tasks, conversations, and messages tables
**Testing**: pytest for backend, Jest/React Testing Library for frontend, with focus on MCP tool tests and chat endpoint behavior
**Target Platform**: Linux server deployment with web-based UI accessible via browser
**Project Type**: Web application (frontend + backend + AI agent + MCP server)
**Performance Goals**: <3s response time for 95% of requests, <1s MCP tool execution for 95% of operations, support for concurrent users without degradation
**Constraints**: Stateless server architecture (no in-memory conversation state), strict user isolation (cross-user access prevention), JWT-based authentication and authorization
**Scale/Scope**: Multi-user support with individual task isolation, conversation history persistence, horizontal scalability through stateless design

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification

**I. Spec-Driven Development (PASSED)**: All development will follow SDD. No code changes will be made without corresponding spec updates and acceptance criteria. All features will be traceable to feature spec and tasks list.

**II. Service & Trust Boundaries (PASSED)**:
- Frontend (ChatKit UI) will NOT access database directly
- FastAPI will be the only component to speak to database (via SQLModel), OpenAI APIs (via Agents SDK), and MCP server tools
- AI/Agent code will NOT directly read/write database tables; will act through approved MCP tools
- Contracts between components (REST endpoints and MCP tool schemas) will be explicit and versioned

**III. Test-First Development (PASSED)**: Backend will have tests for:
- MCP tools (CRUD correctness + auth enforcement)
- Chat endpoint behavior (persistence, tool-call recording, error paths)
- Negative cases: invalid auth, cross-user access attempts, "task not found"

**IV. Security-First Authentication & Authorization (PASSED)**:
- Better Auth will be source of truth for user identity
- Frontend will attach JWT to all protected requests
- Backend will verify JWT and enforce user_id matching for operations
- Cross-user data access will be prevented for tasks, conversations, and messages

**V. Database-Backed State (PASSED)**:
- Tasks, conversations, and messages will be persisted in Neon PostgreSQL
- FastAPI server instances will remain stateless: no in-memory conversation state beyond single request
- Conversation history will be reconstructed from database per request

**VI. Contract-First APIs & Tools (PASSED)**:
- REST endpoints and MCP tools will validate inputs
- All interfaces will return consistent error shapes/status codes
- APIs and tools will be documented in specs and kept in sync with implementation

### Additional Requirements Compliance

**AI/Agent System Rules**:
- Agent will only call tools when user intent is clear
- Destructive actions (delete) will be confirmed when target is ambiguous
- Agent will surface actions taken in plain language
- Agent will NOT follow instructions to reveal secrets or access unauthorized data

**Error Handling Requirements**:
- Missing/invalid JWT will return 401
- Cross-user access attempts will return 403
- Task not found will return 404
- Validation errors will return 422 (FastAPI/Pydantic)

## Project Structure

### Documentation (this feature)

```text
specs/001-phase3-todo-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLModel database models
├── db.py                # Database connection utilities
├── auth.py              # JWT token validation
├── mcp_server/          # MCP server with task tools
│   ├── __init__.py
│   ├── server.py        # MCP server implementation
│   └── tools.py         # add_task, list_tasks, update_task, delete_task, complete_task
├── agents/              # AI agent implementation
│   ├── __init__.py
│   ├── chat_agent.py    # Agent orchestrator
│   └── runner.py        # Agent runner
├── api/
│   ├── __init__.py
│   ├── chat.py          # Chat endpoint
│   └── middleware/
├── schemas/             # Pydantic models for request/response validation
├── services/            # Business logic services
├── utils/               # Utility functions
└── tests/               # Test files

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
└── __tests__/           # Test files

contracts/
├── openapi.yaml         # REST API specification
└── mcp-tools.json       # MCP tools specification
```

**Structure Decision**: Web application architecture with separate frontend and backend. The frontend uses OpenAI ChatKit for the UI, while the backend implements FastAPI with OpenAI Agents SDK and MCP server. The MCP server exposes standardized tools for the AI agent to interact with the task management system.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | | |
