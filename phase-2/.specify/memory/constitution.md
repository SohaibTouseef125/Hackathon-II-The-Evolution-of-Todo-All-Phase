# Todo App Phase II Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All development must follow the Spec-Driven Development methodology. No code may be written without a corresponding specification that has been properly documented in the specs directory. All features must be traced back to specific user stories and acceptance criteria defined in the specification files.

### II. Full-Stack Separation
Frontend and backend code must be properly separated with clear API contracts. The Next.js frontend must communicate with the FastAPI backend through well-defined REST endpoints. No direct database access from the frontend is permitted.

### III. Test-First Development (NON-NEGOTIABLE)
All features must be developed using TDD methodology. Unit tests must be written before implementation code. API endpoints must have integration tests. Frontend components must have appropriate test coverage before being considered complete.

### IV. Security-First Authentication
User authentication and authorization must be implemented using Better Auth with JWT tokens. All API endpoints must validate JWT tokens and enforce user data isolation. No endpoint may be accessible without proper authentication unless explicitly documented as public.

### V. Database-Driven Architecture
All data operations must go through the SQLModel ORM with Neon PostgreSQL as the primary database. Proper database schema design with appropriate indexes, foreign keys, and constraints must be implemented. All database queries must be optimized and follow best practices.

### VI. API-First Design
REST API endpoints must follow consistent patterns with proper HTTP status codes, error handling, and response formats. API contracts must be clearly defined before implementation and maintained throughout the development process.

## Technical Architecture

### Frontend Responsibilities
- Next.js 16+ application using App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Server components by default with client components only when interactivity is required
- API calls must go through a centralized API client
- Proper state management for user interface interactions
- Responsive design for multiple device sizes

### Backend Responsibilities
- FastAPI application for backend services
- SQLModel for ORM operations
- Neon PostgreSQL for data persistence
- JWT token validation middleware
- Proper error handling with HTTPException
- Input validation using Pydantic models
- Database connection management

### Database & Authentication Strategy
- Neon Serverless PostgreSQL as the primary database
- Better Auth for user authentication
- JWT tokens for secure API communication
- User data isolation - each user only accesses their own data
- Proper database indexing for performance
- Secure password storage and handling

### API Design Standards
- RESTful API design with consistent endpoints
- Proper HTTP status codes (200, 201, 400, 401, 404, 500, etc.)
- Consistent response formats
- Input validation and sanitization
- Proper error response structures
- Authentication token validation on all protected endpoints

## Feature Requirements

### Mandatory Features (Basic Level)
- Add Task: Create new todo items with title and description
- Delete Task: Remove tasks from the list by ID
- Update Task: Modify existing task details
- View Task List: Display all tasks with status indicators
- Mark as Complete: Toggle task completion status
- User authentication: Signup, signin, and session management
- User data isolation: Each user only sees their own tasks

### Optional/Bonus Features
- Priorities & Tags/Categories: Assign priority levels or labels to tasks
- Search & Filter: Search by keyword and filter by status
- Sort Tasks: Order by due date, priority, or alphabetically

### User Roles & Permissions
- Registered users: Full CRUD access to their own tasks
- Unauthenticated users: Redirected to login page
- Admin users: Not applicable for Phase II

### Edge Cases & Validations
- Invalid JWT tokens should return 401 Unauthorized
- Attempting to access another user's tasks should return 403 Forbidden
- Missing required fields should return 400 Bad Request
- Non-existent tasks should return 404 Not Found
- Database connection failures should return 500 Internal Server Error

## Development Guidelines

### Coding Standards
- Follow Python PEP 8 and TypeScript/JavaScript style guides
- Use descriptive variable and function names
- Write clear, concise comments for complex logic
- Maintain consistent code formatting using formatters (Black, Prettier)
- Implement proper error handling throughout the application

### Folder & File Structure
- Frontend code in /frontend directory
- Backend code in /backend directory
- Specification files in /specs directory
- Shared configuration in root directory
- Proper separation of concerns in component and module design

### Environment Setup
- Use UV for Python package management
- Use npm/pnpm for frontend dependencies
- Proper .env file handling for environment variables
- Neon PostgreSQL connection configuration
- Better Auth JWT configuration

### Error Handling & Logging
- Centralized error handling in FastAPI
- Proper logging of errors and important events
- User-friendly error messages in the frontend
- Validation errors should be caught and communicated clearly

### Security & Performance Considerations
- JWT token validation on all protected endpoints
- SQL injection prevention through ORM usage
- Input sanitization and validation
- Proper session management
- Performance optimization for database queries
- Secure handling of sensitive data

## UI/UX Requirements

### Design Principles
- Clean, modern user interface
- Intuitive navigation and user flows
- Consistent design language throughout the application
- Mobile-first responsive design approach
- Accessibility compliance (WCAG standards)

### Accessibility Rules
- Proper semantic HTML structure
- ARIA attributes where needed
- Keyboard navigation support
- Sufficient color contrast
- Screen reader compatibility

### Responsive Behavior
- Mobile, tablet, and desktop layouts
- Proper touch targets for mobile devices
- Adaptive grid layouts
- Media query optimization

### Modern UI Expectations
- Smooth transitions and animations
- Loading states for API calls
- Form validation feedback
- Clear visual hierarchy
- Intuitive task management interface

## Milestones & Deliverables

### Step-by-Step Development Roadmap
1. Set up project structure with Next.js frontend and FastAPI backend
2. Implement database schema with SQLModel and Neon PostgreSQL
3. Set up Better Auth authentication with JWT configuration
4. Create API endpoints for task CRUD operations
5. Build frontend components for task management
6. Integrate frontend with backend API
7. Implement user authentication flow
8. Add responsive design and styling
9. Write comprehensive tests
10. Perform integration testing and bug fixes

### Phase-2 Completion Checklist
- [ ] All 5 Basic Level features implemented (Add, Delete, Update, View, Mark Complete)
- [ ] RESTful API endpoints created and tested
- [ ] Responsive frontend interface built
- [ ] Neon Serverless PostgreSQL integration complete
- [ ] Better Auth authentication implemented with JWT
- [ ] User data isolation enforced (each user sees only their tasks)
- [ ] All API endpoints require valid JWT tokens
- [ ] Proper error handling implemented
- [ ] Unit and integration tests written and passing
- [ ] README.md with setup instructions created
- [ ] CLAUDE.md with Claude Code instructions updated
- [ ] Specification files properly maintained

### Testing & Quality Assurance Requirements
- Unit tests for all backend API endpoints
- Integration tests for API functionality
- Frontend component tests where applicable
- End-to-end testing of user flows
- Authentication and authorization testing
- Database operation testing
- Error condition testing

## Evaluation & Completion Criteria

### How Phase-2 Will Be Judged
- Implementation of all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
- Proper use of Spec-Driven Development methodology
- Quality of code architecture and separation of concerns
- Security implementation with proper authentication and user data isolation
- API design quality and consistency
- User interface quality and responsiveness
- Test coverage and quality

### Required Proof of Completion
- GitHub repository with complete source code
- Working web application deployed on Vercel
- Backend API accessible and functional
- Proper authentication flow implemented
- Demo video showing all features working
- Specification files demonstrating spec-driven development process

### What Counts as Incomplete or Disqualified
- Missing any of the 5 Basic Level features
- Lack of proper authentication and user data isolation
- No specification files or evidence of spec-driven development
- Incomplete API implementation
- Non-functional deployed application
- Code that doesn't follow the required technology stack

## Governance

This constitution supersedes all other development practices for Phase II of the Todo App Hackathon. All code changes, architectural decisions, and feature implementations must comply with the principles and requirements outlined above. Any deviations from this constitution must be documented and approved through a formal amendment process.

All pull requests and code reviews must verify compliance with these principles. Code that violates these principles must be rejected or corrected before merging. Complexity must be justified with clear benefits that align with the stated goals.

## Agent and Skill Integration

The following Claude Code agents and skills must be leveraged to ensure compliance with the technical architecture and development standards:

### Required Agents
- **frontend-expert**: Use when building user interfaces, responsive layouts, and accessibility features
- **backend-expert**: Use when implementing API endpoints, database operations, and server-side logic
- **nextjs-expert**: Use when creating Next.js components, pages, and App Router structure
- **auth-flow**: Use when implementing authentication flows, JWT handling, and user session management
- **database-migration**: Use when creating or modifying database schemas and migrations

### Required Skills
- **nextjs-app-router**: Apply when building Next.js applications with App Router architecture
- **fastapi-rest-api**: Apply when creating REST API endpoints with proper validation and error handling
- **sqlmodel-orm**: Apply when defining database models and performing database operations
- **better-auth-integration**: Apply when implementing authentication with Better Auth and JWT verification
- **tailwind-css**: Apply when implementing responsive styling with Tailwind CSS
- **typescript**: Apply when creating type-safe applications with proper interfaces and validation

**Version**: 1.0.0 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-01-03
