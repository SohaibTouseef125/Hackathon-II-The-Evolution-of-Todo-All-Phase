# AGENTS.md

Ye guide batata hai kaun sa agent kaun si skills use karta hai, har skill ka role kya hai, aur kab use karna chahiye.

---

## USER-LEVEL AGENTS ( ~/.claude/agents/ )

### 1. frontend-expert

| Property | Value |
|----------|-------|
| **Skills** | `frontend-expert`, `frontend-design`, `tailwindcss-v4`, `ui-ux-design` |
| **Model** | sonnet |
| **Color** | red |

**Role:** Building user interfaces, responsive designs, web performance, accessibility compliance.

**Why These Skills:**
- `frontend-expert` → Core frontend patterns
- `frontend-design` → Design implementation
- `tailwindcss-v4` → Tailwind CSS styling
- `ui-ux-design` → UX/UI best practices

**Use When:**
- Creating new UI components or pages
- Debugging layout or styling issues
- Implementing responsive designs
- Web performance optimization
- Accessibility improvements

---

### 2. backend-expert

| Property | Value |
|----------|-------|
| **Skills** | `backend-expert` |
| **Model** | sonnet |
| **Color** | blue |

**Role:** Backend development, API design, database operations, server-side logic.

**Why These Skills:**
- `backend-expert` → Server architecture, Node.js/Express, security patterns

**Use When:**
- Building REST APIs
- Database schema design
- Authentication middleware
- Server-side business logic

---

### 3. nextjs-expert

| Property | Value |
|----------|-------|
| **Skills** | `nextjs-16`, `react.js-latest`, `tailwindcss-v4`, `ui-ux-design` |
| **Model** | sonnet |
| **Color** | yellow |

**Role:** Next.js 15+ development with App Router, Server Components, modern patterns.

**Why These Skills:**
- `nextjs-16` → App Router, SSR/SSG/ISR patterns
- `react.js-latest` → React hooks, components
- `tailwindcss-v4` → Styling
- `ui-ux-design` → UX best practices

**Use When:**
- Creating Next.js pages with App Router
- Implementing Server Actions
- Data fetching patterns
- Performance optimization

---

### 4. react-expert

| Property | Value |
|----------|-------|
| **Skills** | `react.js-latest`, `tailwindcss-v4`, `ui-ux-design` |
| **Model** | sonnet |
| **Color** | pink |

**Role:** React development, component architecture, state management.

**Why These Skills:**
- `react.js-latest` → React 18+ features, hooks
- `tailwindcss-v4` → Component styling
- `ui-ux-design` → Design patterns

**Use When:**
- Building React components
- Complex state management
- React performance optimization
- Component refactoring

---

### 5. typescript-expert

| Property | Value |
|----------|-------|
| **Skills** | `typescript` |
| **Model** | sonnet |
| **Color** | cyan |

**Role:** TypeScript development, type safety, advanced TypeScript patterns.

**Why These Skills:**
- `typescript` → Type safety, generics, interfaces

**Use When:**
- Writing TypeScript code
- Creating type definitions
- Migrating JS to TS
- Debugging type errors

---

### 6. css-expert

| Property | Value |
|----------|-------|
| **Skills** | `css-expert` |
| **Model** | sonnet |
| **Color** | purple |

**Role:** CSS, Tailwind CSS, responsive design, styling best practices.

**Why These Skills:**
- `css-expert` → Modern CSS, layouts, animations

**Use When:**
- Complex CSS layouts
- Animations
- Responsive design
- CSS debugging

---

### 7. javascript-expert

| Property | Value |
|----------|-------|
| **Skills** | `javascript` |
| **Model** | sonnet |
| **Color** | yellow |

**Role:** Modern ES6+ JavaScript, frontend/backend JavaScript.

**Why These Skills:**
- `javascript` → ES6+ features, async patterns

**Use When:**
- Writing JavaScript code
- Debugging JS issues
- Modern ES6+ refactoring

---

### 8. tailwind-expert

| Property | Value |
|----------|-------|
| **Skills** | `ui-ux-design`, `tailwindcss-v4` |
| **Model** | sonnet |
| **Color** | pink |

**Role:** Tailwind CSS implementation, utility-first styling, responsive design.

**Why These Skills:**
- `ui-ux-design` → Design principles
- `tailwindcss-v4` → Tailwind utility classes

**Use When:**
- Tailwind CSS implementation
- Custom component patterns
- Responsive Tailwind layouts

---

### 9. uiux-expert

| Property | Value |
|----------|-------|
| **Skills** | `ui-ux-design`, `tailwindcss-v4` |
| **Model** | sonnet |
| **Color** | pink |

**Role:** UI/UX design principles, user experience, interface design.

**Why These Skills:**
- `ui-ux-design` → Design research, accessibility
- `tailwindcss-v4` → Implementation

**Use When:**
- Designing new interfaces
- UX reviews
- Accessibility compliance
- Design systems

---

### 10. database-migration

| Property | Value |
|----------|-------|
| **Skills** | `neon-serverless-database`, `sqlmodel-orm` |
| **Color** | Purple |

**Role:** Database schema changes, migrations, data management.

**Why These Skills:**
- `neon-serverless-database` → Neon Postgres
- `sqlmodel-orm` → SQLModel/Alembic migrations

**Use When:**
- Setting up Alembic migrations
- Schema changes
- Database versioning

---

### 11. api-endpoint-generator

| Property | Value |
|----------|-------|
| **Skills** | `fastapi-rest-api` |
| **Color** | Green |

**Role:** Creating REST API endpoints with FastAPI, validation, error handling.

**Why These Skills:**
- `fastapi-rest-api` → FastAPI CRUD, Pydantic models

**Use When:**
- Generating CRUD endpoints
- API model creation
- FastAPI implementation

---

### 12. auth-flow

| Property | Value |
|----------|-------|
| **Skills** | `better-auth-integration` |
| **Color** | Orange |

**Role:** Authentication with Better Auth + JWT verification in FastAPI.

**Why These Skills:**
- `better-auth-integration` → Better Auth setup, JWT tokens

**Use When:**
- Login/signup implementation
- Protected routes
- Session management

---

### 13. fullstack-scaffold

| Property | Value |
|----------|-------|
| **Skills** | `full-stack-expert` |
| **Color** | Blue |

**Role:** Creating complete monorepo structure for Next.js + FastAPI.

**Why These Skills:**
- `full-stack-expert` → Fullstack architecture patterns

**Use When:**
- New project initialization
- Monorepo setup
- Complete scaffold generation

---

### 14. fullstack-integrator

| Property | Value |
|----------|-------|
| **Skills** | `full-stack-expert`, `frontend-design`, `frontend-expert`, `backend-expert` |
| **Model** | sonnet |
| **Color** | green |

**Role:** End-to-end features, frontend-backend integration, API contracts.

**Why These Skills:**
- `full-stack-expert` → Integration patterns
- `frontend-design` + `frontend-expert` → UI side
- `backend-expert` → API side

**Use When:**
- API integration
- Fullstack feature implementation
- Data flow debugging

---

### 15. mern-specialist

| Property | Value |
|----------|-------|
| **Skills** | `mern-stack` |
| **Model** | sonnet |
| **Color** | yellow |

**Role:** MERN stack (MongoDB, Express, React, Node.js) development.

**Why These Skills:**
- `mern-stack` → MongoDB, Express, React, Node

**Use When:**
- MERN application development
- CRUD operations
- JWT authentication in MERN

---

### 16. openai-agents-expert

| Property | Value |
|----------|-------|
| **Skills** | `openai-agents-sdk` |
| **Model** | sonnet |
| **Color** | cyan |

**Role:** OpenAI API integration, agent development, tool calling.

**Why These Skills:**
- `openai-agents-sdk` → OpenAI Agents SDK patterns

**Use When:**
- Building AI agents
- OpenAI API integration
- Multi-agent systems

---

## PROJECT-LEVEL AGENTS ( .claude/agents/ )

### 17. chatbot-implementation

| Property | Value |
|----------|-------|
| **Skills** | `openai-chatkit` |
| **Color** | Green |

**Role:** Complete AI chatbot with OpenAI ChatKit UI + Agents SDK + MCP.

**Why These Skills:**
- `openai-chatkit` → ChatKit frontend integration

**Use When:**
- Chatbot UI implementation
- Conversation management
- Fullstack chatbot systems

---

### 18. lead-phase3-architect

| Property | Value |
|----------|-------|
| **Skills** | `mcp-server-python`, `openai-agents-sdk`, `openai-chatkit`, `phase3-todo-chatbot` |
| **Model** | sonnet |
| **Color** | red |

**Role:** Phase 3 infrastructure - FastAPI + Agents SDK + MCP + Neon DB.

**Why These Skills:**
- `mcp-server-python` → MCP server development
- `openai-agents-sdk` → Agent patterns
- `openai-chatkit` → Frontend chat
- `phase3-todo-chatbot` → Todo chatbot specific

**Use When:**
- Phase 3 backend setup
- MCP tool development
- Core feature architecture

---

### 19. mcp-task-tools

| Property | Value |
|----------|-------|
| **Skills** | `mcp-server-python` |
| **Model** | sonnet |
| **Color** | blue |

**Role:** Stateless MCP tools for task CRUD (JSON-only output).

**Why These Skills:**
- `mcp-server-python` → MCP tool implementation

**Use When:**
- MCP tool creation
- Database-backed CRUD operations
- Structured JSON responses

---

### 20. todo-chat-agent

| Property | Value |
|----------|-------|
| **Skills** | (inherits from MCP tools) |
| **Model** | sonnet |
| **Color** | red |

**Role:** Conversational interface for todo management via MCP tools.

**Why These Skills:**
- Uses MCP tools (add_task, list_tasks, etc.) for operations

**Use When:**
- Natural language todo requests
- Multi-step todo workflows
- User confirmation flows

---

### 21. urdu-linguistic-expert

| Property | Value |
|----------|-------|
| **Skills** | `urdu-support` |
| **Model** | sonnet |
| **Color** | blue |

**Role:** Urdu/Roman Urdu language support, intent mapping, RTL UI.

**Why These Skills:**
- `urdu-support` → Urdu linguistics, RTL support

**Use When:**
- Urdu language processing
- Roman Urdu intent mapping
- RTL UI implementation

---

### 22. voice-analytics-expert

| Property | Value |
|----------|-------|
| **Skills** | `voice-command-processor`, `search-analytics` |
| **Model** | sonnet |
| **Color** | green |

**Role:** Voice transcript processing, productivity analytics, summaries.

**Why These Skills:**
- `voice-command-processor` → STT processing
- `search-analytics` → Task metrics

**Use When:**
- Voice transcript cleanup
- Productivity summaries
- Task completion analytics

---

## ALL SKILLS REFERENCE

### User-Level Skills

| Skill | Role |
|-------|------|
| `backend-expert` | Server architecture, Node.js, Express, security |
| `frontend-expert` | Frontend patterns, performance, accessibility |
| `frontend-design` | Design implementation, responsive layouts |
| `full-stack-expert` | Fullstack patterns, architecture, integration |
| `nextjs-16` | Next.js 15+ App Router, Server Components |
| `react.js-latest` | React 18+ hooks, state management, components |
| `tailwindcss-v4` | Tailwind CSS utility classes, responsive design |
| `ui-ux-design` | UX principles, accessibility, design research |
| `css-expert` | Modern CSS, animations, layouts |
| `javascript` | ES6+ features, async patterns |
| `typescript` | Type safety, generics, advanced types |
| `mern-stack` | MongoDB, Express, React, Node.js |
| `fastapi-rest-api` | FastAPI CRUD, Pydantic models |
| `neon-serverless-database` | Neon PostgreSQL serverless |
| `sqlmodel-orm` | SQLModel, Alembic migrations |
| `better-auth-integration` | Better Auth, JWT tokens |
| `openai-agents-sdk` | OpenAI Agents SDK, tool calling |

### Project-Level Skills

| Skill | Role |
|-------|------|
| `mcp-server-python` | MCP Python SDK, tool exposure |
| `openai-chatkit` | OpenAI ChatKit UI |
| `phase3-todo-chatbot` | Phase 3 todo chatbot patterns |
| `search-analytics` | Task metrics, analytics |
| `skill-creator` | Creating new skills |
| `stateless-chatbot-architecture` | Stateless chatbot patterns |
| `todo-ai-chatbot` | Todo AI chatbot |
| `urdu-support` | Urdu/Roman Urdu support |
| `voice-command-processor` | Voice transcript processing |

---

## QUICK REFERENCE: WHEN TO USE WHICH AGENT

| Task Type | Recommended Agent |
|-----------|------------------|
| UI Components | `frontend-expert`, `react-expert` |
| Next.js Project | `nextjs-expert` |
| REST API (FastAPI) | `api-endpoint-generator` |
| Database Migrations | `database-migration` |
| Authentication | `auth-flow` |
| Fullstack Integration | `fullstack-integrator` |
| MERN Stack | `mern-specialist` |
| AI Agents | `openai-agents-expert` |
| Chatbot (Phase 3) | `lead-phase3-architect` |
| MCP Tools | `mcp-task-tools` |
| Todo Chatbot | `todo-chat-agent` |
| Urdu Support | `urdu-linguistic-expert` |
| Voice Analytics | `voice-analytics-expert` |
| New Project Scaffold | `fullstack-scaffold` |
| CSS/Tailwind | `css-expert`, `tailwind-expert` |
| UI/UX Design | `uiux-expert` |
| TypeScript | `typescript-expert` |
| JavaScript | `javascript-expert` |

---

## AGENT-SKILL MATRIX

| Agent | Skills |
|-------|--------|
| `frontend-expert` | frontend-expert, frontend-design, tailwindcss-v4, ui-ux-design |
| `backend-expert` | backend-expert |
| `nextjs-expert` | nextjs-16, react.js-latest, tailwindcss-v4, ui-ux-design |
| `react-expert` | react.js-latest, tailwindcss-v4, ui-ux-design |
| `typescript-expert` | typescript |
| `css-expert` | css-expert |
| `javascript-expert` | javascript |
| `tailwind-expert` | ui-ux-design, tailwindcss-v4 |
| `uiux-expert` | ui-ux-design, tailwindcss-v4 |
| `database-migration` | neon-serverless-database, sqlmodel-orm |
| `api-endpoint-generator` | fastapi-rest-api |
| `auth-flow` | better-auth-integration |
| `fullstack-scaffold` | full-stack-expert |
| `fullstack-integrator` | full-stack-expert, frontend-design, frontend-expert, backend-expert |
| `mern-specialist` | mern-stack |
| `openai-agents-expert` | openai-agents-sdk |
| `chatbot-implementation` | openai-chatkit |
| `lead-phase3-architect` | mcp-server-python, openai-agents-sdk, openai-chatkit, phase3-todo-chatbot |
| `mcp-task-tools` | mcp-server-python |
| `todo-chat-agent` | (uses MCP tools) |
| `urdu-linguistic-expert` | urdu-support |
| `voice-analytics-expert` | voice-command-processor, search-analytics |
