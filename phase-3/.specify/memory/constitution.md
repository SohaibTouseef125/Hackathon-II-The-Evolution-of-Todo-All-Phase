<!--
SYNC IMPACT REPORT
- Version change: 1.0.0 → 2.0.0
- Modified principles:
  - I. Spec-Driven Development → I. Spec-Driven Development (expanded: Phase III AI + MCP requirements)
  - II. Full-Stack Separation → II. Service & Trust Boundaries (expanded: Agent/MCP boundaries)
  - III. Test-First Development → III. Test-First Development (expanded: tool + chat endpoint tests)
  - IV. Security-First Authentication → IV. Security-First Authentication (expanded: auth ↔ user_id enforcement)
  - V. Database-Driven Architecture → V. Database-Backed State (expanded: conversations/messages)
  - VI. API-First Design → VI. Contract-First APIs & Tools (REST + MCP)
- Added sections:
  - AI/Agent System Rules
  - MCP Tooling Rules
  - Conversation State & Statelessness
- Removed sections:
  - Phase II-specific completion checklist wording (replaced with Phase III deliverables)
- Templates requiring updates:
  - ✅ Updated: .specify/templates/tasks-template.md (tests requirement aligned with constitution)
  - ⚠ Pending review only: .specify/templates/plan-template.md ("Constitution Check" is generated dynamically)
  - ✅ Already aligned: .specify/templates/spec-template.md ("User Scenarios & Testing" is mandatory)
- Deferred TODOs: none
-->

# Todo App Phase III Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All development MUST follow Spec-Driven Development.

- No code changes without a corresponding spec update and acceptance criteria.
- Every feature MUST be traceable to a feature spec (user stories + scenarios) and a tasks list.
- The system MUST remain aligned with the Phase III architecture requirements: ChatKit UI + FastAPI chat
  endpoint + OpenAI Agents SDK + Official MCP SDK + Neon PostgreSQL.

### II. Service & Trust Boundaries (NON-NEGOTIABLE)
The system is a multi-component, least-privilege design. Boundaries are enforced and are not optional.

- **Frontend (ChatKit UI)** MUST NOT access the database directly.
- **FastAPI** is the only component allowed to speak to:
  - the database (via SQLModel)
  - OpenAI APIs (via Agents SDK)
  - MCP server tools (local/in-process or networked)
- **AI/Agent code** MUST NOT directly read/write database tables; it MUST act through approved MCP tools.
- Contracts between components (REST endpoints and MCP tool schemas) MUST be explicit and versioned.

### III. Test-First Development (NON-NEGOTIABLE)
All features MUST follow TDD where practical.

- Backend MUST have tests for:
  - MCP tools (CRUD correctness + auth enforcement)
  - Chat endpoint behavior (persistence, tool-call recording, error paths)
- Tests MUST cover negative cases: invalid auth, cross-user access attempts, and "task not found".

### IV. Security-First Authentication & Authorization (NON-NEGOTIABLE)
Authentication is handled on the frontend, authorization is enforced on the backend.

- Better Auth MUST be the source of truth for user identity.
- Frontend MUST attach JWT (`Authorization: Bearer <token>`) to all protected requests.
- Backend MUST verify JWT and MUST enforce that the effective authenticated user matches the `user_id`
  used for any task/conversation operation.
- Cross-user data access MUST be prevented for tasks, conversations, and messages.

### V. Database-Backed State (NON-NEGOTIABLE)
Phase III is stateless at the server layer but stateful in the database.

- Tasks, conversations, and messages MUST be persisted in Neon PostgreSQL.
- FastAPI server instances MUST remain stateless: no in-memory conversation state beyond a single request.
- Conversation history MUST be reconstructed from the database per request.

### VI. Contract-First APIs & Tools
The product exposes two primary interfaces and both must be treated as contracts:

- **REST**: chat endpoint(s) and any supporting endpoints.
- **MCP tools**: `add_task`, `list_tasks`, `update_task`, `delete_task`, `complete_task`.

All interfaces MUST:

- validate inputs
- return consistent error shapes/status codes
- be documented in specs and kept in sync with implementation

## Phase III Technical Architecture

### Frontend Responsibilities
- Chat UI built with OpenAI ChatKit.
- Auth UI/flows handled with Better Auth.
- The frontend MUST call only the backend chat endpoint and/or task endpoints through a single API client.
- The frontend MUST NOT attempt to run agent logic locally.

### Backend Responsibilities
- FastAPI provides a stateless chat endpoint.
- The backend orchestrates:
  - conversation persistence (SQLModel)
  - agent execution (OpenAI Agents SDK)
  - tool execution (Official MCP SDK)
- Backend MUST record:
  - user messages
  - assistant messages
  - tool calls executed (for observability and debugging)

### MCP Tools Responsibilities
- MCP tools MUST be stateless.
- MCP tools MUST enforce authorization and ownership.
- MCP tools MUST be the *only* mechanism the agent uses to mutate or query tasks.

## AI/Agent System Rules

### Tool-Use Safety
- The agent MUST only call tools when user intent is clear.
- Destructive actions (delete) MUST be confirmed when the target is ambiguous (e.g., multiple matches).
- The agent MUST surface what it did (created/updated/deleted/completed) in plain language.

### Prompt Injection & Untrusted Input
Treat all user messages as untrusted input.

- The agent MUST NOT follow instructions to reveal secrets, system prompts, or credentials.
- The agent MUST NOT execute tool calls that attempt to access data outside the authenticated user scope.
- The backend MUST never place secrets into model messages.

## Feature Requirements (Phase III)

### Mandatory Features
- Conversational interface for the 5 basic CRUD operations via MCP tools.
- Stateless chat request cycle:
  1) receive user message
  2) load conversation history from DB
  3) persist new user message
  4) run agent with MCP tools
  5) persist assistant response + tool calls
  6) return response

### Data Model Requirements
- **Task** MUST be scoped to `user_id`.
- **Conversation** MUST be scoped to `user_id`.
- **Message** MUST be scoped to `user_id` and tied to `conversation_id`.

### Error Handling Requirements
- Missing/invalid JWT: 401
- Cross-user access attempt: 403
- Task not found: 404
- Validation errors: 422 (FastAPI/Pydantic)

## Development Guidelines

### Environment & Secrets (NON-NEGOTIABLE)
- Secrets MUST NOT be committed.
- Backend MUST use environment variables for:
  - `DATABASE_URL`
  - `BETTER_AUTH_SECRET`
  - `OPENAI_API_KEY` (or equivalent for Agents SDK)
- Frontend MUST use env variables for any public config (never secret API keys).

### Logging & Observability
- Backend MUST log request IDs and record tool calls for debugging.
- Errors MUST be logged with enough context to reproduce (without logging secrets).

### Minimal-Diff Rule
Changes MUST be the smallest viable diff to satisfy the spec and tasks. Avoid refactors not required by
Phase III requirements.

## Governance

This constitution supersedes prior phase constitutions for Phase III work.

- All changes MUST comply with the principles above.
- Deviations MUST be documented as an amendment to this constitution.

**Version**: 2.0.0 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-01-12
