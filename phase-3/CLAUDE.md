# Todo App Phase III - AI Chatbot Development

## Project Overview

This project implements a Todo AI Chatbot as part of the Hackathon II evolution of Todo applications. The system transforms the existing todo web application into an intelligent conversational interface using OpenAI ChatKit, FastAPI, OpenAI Agents SDK, Official MCP SDK, and Neon PostgreSQL.

## Phase III Architecture

The current focus is Phase III: Todo AI Chatbot with these key components:
- **Frontend**: OpenAI ChatKit UI utilizing ChatKit widgets for natural language interaction and conversation history management
- **Backend**: FastAPI server with pluggable AI agent architecture (currently OpenAI Agents SDK, extensible to other providers) and MCP server
- **Database**: Neon Serverless PostgreSQL for persistence and conversation history preservation
- **Authentication**: Better Auth with JWT tokens
- **MCP Tools**: Standardized interface for AI to interact with task operations

## Key Technologies

- Python 3.13+, FastAPI, SQLModel, Neon PostgreSQL
- Next.js 16+, TypeScript 5+, OpenAI ChatKit
- OpenAI Agents SDK, Official MCP SDK (with architecture supporting other AI providers)
- Better Auth for authentication
- Spec-Kit Plus for specification management

## Project Structure

- `/frontend` - Next.js 16 app with OpenAI ChatKit
- `/backend` - Python FastAPI server with OpenAI Agents SDK and MCP tools
- `/specs` - Specification files for all features
- `/contracts` - API and MCP tool specifications

## Development Workflow

1. **Specification Phase**: Use `/sp.specify` to create feature specs
2. **Planning Phase**: Use `/sp.plan` to generate architecture plans
3. **Tasks Phase**: Use `/sp.tasks` to break down implementation
4. **Implementation**: Follow spec-driven development principles

## Spec-Kit Structure

Specifications are organized in /specs:
- `/specs/overview.md` - Project overview
- `/specs/features/` - Feature specs (what to build)
- `/specs/api/` - API endpoint and MCP tool specs
- `/specs/database/` - Schema and model specs
- `/specs/ui/` - Component and page specs

## How to Use Specs

1. Always read relevant spec before implementing
2. Reference specs with: @specs/features/[feature].md
3. Update specs if requirements change

## Commands

- Frontend: cd frontend && npm run dev
- Backend: cd backend && uvicorn main:app --reload --port 8000
- Backend with MCP: cd backend && python -m mcp_server
- Tests: Run pytest in backend and jest in frontend

---

## Available Agents and Skills

Agents and Skills are specialized capabilities that extend Claude's functionality. Use them proactively when relevant conditions are detected.

### USER-LEVEL AGENTS (from ~/.claude/agents/)

These agents are globally available and should be invoked when specific conditions are detected.

---

#### 1. frontend-expert
**When to invoke:** When building/modifying user interfaces, debugging layout issues, implementing responsive designs, optimizing web performance, ensuring accessibility compliance, or working with HTML/CSS/JavaScript.

**Examples:**
- "Create a responsive navigation bar with mobile menu"
- "Debug sidebar overlapping on tablet screens"
- "Implement user profile page with avatar upload"

**Skills:** `frontend-expert`, `frontend-design`, `tailwindcss-v4`, `ui-ux-design`

---

#### 2. backend-expert
**When to invoke:** When working on backend development, building/modifying APIs, implementing authentication/authorization, designing database schemas, optimizing queries, handling server-side business logic, or backend security.

**Examples:**
- "Create user registration API endpoint"
- "Optimize slow database queries"
- "Add JWT authentication middleware"

**Skills:** `backend-expert`

---

#### 3. nextjs-expert
**When to invoke:** When building Next.js applications, implementing SSR/SSG/ISR strategies, working with App Router/Server Components, creating Server Actions, optimizing Next.js performance, or handling data fetching patterns.

**Examples:**
- "Create product listing page with SSG"
- "Implement contact form with Server Actions"
- "Optimize slow Next.js bundle size"

**Skills:** `nextjs-16`, `react.js-latest`, `tailwindcss-v4`, `ui-ux-design`

---

#### 4. react-expert
**When to invoke:** When building React components, debugging React issues, optimizing React performance, implementing complex UI logic, refactoring React code, or setting up React architecture.

**Examples:**
- "Create user profile component with form validation"
- "Dashboard re-rendering too frequently"
- "Refactor complex component with too much logic"

**Skills:** `react.js-latest`, `tailwindcss-v4`, `ui-ux-design`

---

#### 5. typescript-expert
**When to invoke:** When writing TypeScript code, creating type definitions, migrating JavaScript to TypeScript, debugging type errors, implementing generics, or refactoring for type safety.

**Examples:**
- "Create typed API fetch function"
- "Fix TypeScript type error"
- "Convert JavaScript utility to TypeScript"

**Skills:** `typescript`

---

#### 6. css-expert
**When to invoke:** When working with CSS styling, layout implementation, responsive design, animations, or debugging CSS-related issues.

**Examples:**
- "Create responsive card component"
- "Navigation bar not centering properly"
- "Add smooth hover animations"

**Skills:** `css-expert`

---

#### 7. javascript-expert
**When to invoke:** When writing JavaScript code, debugging JavaScript issues, implementing complex JavaScript logic, or using modern ES6+ features.

**Examples:**
- "Create function to filter array of users"
- "Debug async function returning undefined"
- "Refactor jQuery to modern vanilla JavaScript"

**Skills:** `javascript`

---

#### 8. tailwind-expert
**When to invoke:** When implementing/modifying Tailwind CSS styling, creating reusable component patterns, optimizing Tailwind configurations, or needing guidance on responsive design and utility-first best practices.

**Examples:**
- "Create responsive card with hover effects"
- "Configure Tailwind with custom colors"
- "Make layout work on mobile and desktop"

**Skills:** `ui-ux-design`, `tailwindcss-v4`

---

#### 9. uiux-expert
**When to invoke:** When designing/reviewing user interfaces, conducting UX research, improving user experience, ensuring accessibility compliance, creating design systems, or making design decisions.

**Examples:**
- "Design analytics dashboard"
- "Review checkout flow for UX best practices"
- "Make modal keyboard accessible"

**Skills:** `ui-ux-design`, `tailwindcss-v4`

---

#### 10. database-migration
**When to invoke:** When setting up/configuring Alembic migrations with SQLModel, generating migration scripts, applying migrations, or managing schema changes.

**Examples:**
- "Initialize Alembic for new project"
- "Generate migration from model changes"
- "Perform zero-downtime deployment migration"

**Skills:** `neon-serverless-database`, `sqlmodel-orm`

---

#### 11. api-endpoint-generator
**When to invoke:** When generating complete FastAPI CRUD endpoints with request/response models, error handling, JWT authentication, and tests from API specifications.

**Examples:**
- "Generate CRUD endpoints for tasks resource"
- "Create Pydantic models and routes"
- "Generate tests for API endpoints"

**Skills:** `fastapi-rest-api`

---

#### 12. auth-flow
**When to invoke:** When implementing complete authentication flow with Better Auth in Next.js and JWT verification in FastAPI, including signup/login pages, protected routes, and API authentication.

**Examples:**
- "Set up user registration with Better Auth"
- "Implement JWT token verification in FastAPI"
- "Create protected route middleware"

**Skills:** `better-auth-integration`

---

#### 13. fullstack-scaffold
**When to invoke:** When generating complete monorepo structure for Next.js + FastAPI applications with proper organization, configuration, and documentation.

**Examples:**
- "Create new Next.js + FastAPI project"
- "Generate monorepo with Docker Compose"
- "Set up complete project structure"

**Skills:** `full-stack-expert`

---

#### 14. fullstack-integrator
**When to invoke:** When implementing complete end-to-end features, integrating frontend UI with backend APIs, designing API contracts, implementing authentication flows, debugging full-stack issues, or setting up real-time communication.

**Examples:**
- "Connect login form to backend API"
- "Debug data not flowing from backend to frontend"
- "Implement profile picture upload"

**Skills:** `full-stack-expert`, `frontend-design`, `frontend-expert`, `backend-expert`

---

#### 15. mern-specialist
**When to invoke:** When building MERN stack applications, implementing CRUD operations, connecting React to Express APIs, designing MongoDB schemas, or implementing JWT authentication.

**Examples:**
- "Create user registration in MERN app"
- "Build CRUD API for products"
- "Fix CORS errors between React and Express"

**Skills:** `mern-stack`

---

#### 16. openai-agents-expert
**When to invoke:** When building AI agents, integrating OpenAI APIs, implementing tool calling, or designing agentic systems.

**Examples:**
- "Build research agent with web search"
- "Implement streaming responses"
- "Design multi-agent system"

**Skills:** `openai-agents-sdk`

---

### PROJECT-LEVEL AGENTS (from .claude/agents/)

These agents are specific to the current project and should be invoked when relevant conditions are met.

**Important:** Some agent names also exist at the user-level (e.g., `auth-flow`, `api-endpoint-generator`, `database-migration`). When selecting an agent, prefer the project-level one if you are working inside this repo and it matches the task.

**Important:** This repo also has additional *user-level* agents available in `~/.claude/agents/` (not checked into git). Those user-level agents include: `docker-agent`, `docker-container-specialist`, `database-agent`, `pytest-agent`, `fastapi-dev-agent`, `k8s-manifest-specialist`, `ui-animations-agent`, `ui-component-library`, `responsive-design-agent`.

**Note:** The actual list should always be derived from frontmatter in these directories:
- Personal: `/home/sohaib/.claude/agents/`
- Project: `/mnt/d/phase-3/.claude/agents/`

---

#### 17. chatbot-implementation
**When to invoke:** When implementing complete AI chatbot systems with OpenAI ChatKit UI, OpenAI Agents SDK, MCP server integration, and conversation management.

**Examples:**
- "Create chatbot with ChatKit UI"
- "Implement conversation persistence"
- "Set up MCP tool integration"

**Skills:** `openai-chatkit`

---

#### 18. lead-phase3-architect
**When to invoke:** When implementing or modifying Phase 3 infrastructure, including FastAPI backend, OpenAI Agents SDK integration, MCP server development, or Neon Database persistence.

**Examples:**
- "Setup initial FastAPI backend with Agents SDK"
- "Add new tool to MCP server"
- "Implement Phase 3 database layer"

**Skills:** `mcp-server-python`, `openai-agents-sdk`, `openai-chatkit`, `phase3-todo-chatbot`

---

#### 19. mcp-task-tools
**When to invoke:** When you need to expose or invoke stateless MCP tools that perform validated database-backed CRUD operations for tasks with structured JSON-only output.

**Examples:**
- "Add a new task via MCP tool"
- "List all incomplete tasks"
- "Mark task as completed"

**Skills:** `mcp-server-python`

---

#### 20. todo-chat-agent
**When to invoke:** When you need a primary conversational interface that translates natural-language requests into todo CRUD actions via MCP tools.

**Examples:**
- "I need to remember to pay bills"
- "Delete the groceries task"
- "Change my dentist reminder"

**Skills:** (uses MCP tools: add_task, list_tasks, update_task, delete_task, complete_task)

---

#### 21. urdu-linguistic-expert
**When to invoke:** When you need to implement/verify Urdu and Roman Urdu language support, map natural-language intents to tools, or design localized UIs with RTL support.

**Examples:**
- "Verify agent understands 'Subah 9 baje meeting rakhdo'"
- "Create greeting component in Urdu script"
- "Implement RTL support for Urdu UI"

**Skills:** `urdu-support`

---

#### 22. voice-analytics-expert
**When to invoke:** When processing voice transcripts, requesting daily productivity summaries, or asking for task completion analytics.

**Examples:**
- "Clean this voice transcript"
- "How was my productivity today?"
- "Generate daily summary of tasks"

**Skills:** `voice-command-processor`, `search-analytics`

---

### USER-LEVEL SKILLS (from ~/.claude/skills/)

Skills are reusable capabilities that provide specialized knowledge and patterns.

| Skill | When to Use |
|-------|-------------|
| `backend-expert` | Server architecture, Node.js/Express, security patterns |
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

---

### PROJECT-LEVEL SKILLS (from .claude/skills/)

| Skill | When to Use |
|-------|-------------|
| `mcp-server-python` | MCP Python SDK, tool exposure |
| `openai-chatkit` | OpenAI ChatKit UI integration |
| `phase3-todo-chatbot` | Phase 3 todo chatbot patterns |
| `search-analytics` | Task metrics, analytics |
| `skill-creator` | Creating new skills |
| `stateless-chatbot-architecture` | Stateless chatbot patterns |
| `todo-ai-chatbot` | Todo AI chatbot |
| `urdu-support` | Urdu/Roman Urdu support |
| `voice-command-processor` | Voice transcript processing |
| `fastapi-development` | FastAPI, Pydantic, SQLModel, JWT auth |
| `ui-component-library` | Reusable UI components, forms, data display |
| `ui-animations` | CSS animations, Framer Motion, micro-interactions |
| `ui-responsive-design` | Mobile-first, CSS Grid, Flexbox, breakpoints |
| `docker-development` | Dockerfile, Docker Compose, containerization |
| `pytest-testing` | Pytest patterns, fixtures, mocking, FastAPI testing |
| `database-development` | PostgreSQL schema, indexing, migrations, ops |

---

### Automatic Agent Invocation

Invoke agents proactively when the following conditions are detected:

#### Frontend Work
- UI component creation → `frontend-expert`
- React component → `react-expert`
- Next.js page/route → `nextjs-expert`
- Tailwind styling → `tailwind-expert`
- CSS layouts → `css-expert`
- Design/UX review → `uiux-expert`

#### Backend Work
- REST API creation → `api-endpoint-generator`
- Database migrations → `database-migration`
- Authentication → `auth-flow`
- General backend → `backend-expert`
- FastAPI work → `fastapi-development` skill

#### Fullstack Work
- New project scaffold → `fullstack-scaffold`
- API integration → `fullstack-integrator`
- MERN stack → `mern-specialist`

#### AI/Agent Work
- OpenAI integration → `openai-agents-expert`
- Chatbot UI → `chatbot-implementation`
- Phase 3 architecture → `lead-phase3-architect`
- MCP tools → `mcp-task-tools`
- Todo conversation → `todo-chat-agent`

#### Language/Localization
- Urdu/Roman Urdu → `urdu-linguistic-expert`
- Voice transcripts → `voice-analytics-expert`

#### Code Quality
- TypeScript → `typescript-expert`
- JavaScript → `javascript-expert`
