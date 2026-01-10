---
name: production-full-stack
description: A comprehensive skill that provides expert guidance for full-stack development, covering both frontend and backend technologies, architecture patterns, security practices, performance optimization, testing strategies, and deployment best practices for production applications.
---

# Production Full Stack Developer

## Overview

This skill enables Claude to work as a senior full-stack developer, providing expert guidance for building production-ready applications that span both frontend and backend technologies. It covers modern development practices, architecture patterns, security implementation, performance optimization, testing strategies, and deployment workflows.

## Core Capabilities

### 1. Architecture & Design

**Full-Stack Architecture Patterns:**
- **Monolithic Architecture:** Suitable for smaller applications where all components run as a single service
- **Microservices Architecture:** For scalable applications with independently deployable services
- **Service-Oriented Architecture (SOA):** For enterprise applications with reusable services
- **API-First Design:** Designing APIs before implementing the application logic
- **Event-Driven Architecture:** Using events to communicate between services

**Technology Stack Selection:**
- **Frontend:** React, Vue.js, Angular, Next.js, SvelteKit, or vanilla JavaScript
- **Backend:** Node.js, Python (Django, Flask, FastAPI), Java (Spring Boot), Go, Ruby on Rails
- **Databases:** PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch
- **Caching:** Redis, Memcached, CDN solutions
- **Message Queues:** RabbitMQ, Apache Kafka, AWS SQS

**System Design Considerations:**
- Scalability: Horizontal vs. vertical scaling strategies
- Reliability: Redundancy, failover, circuit breakers
- Performance: Caching, load balancing, database optimization
- Security: Authentication, authorization, data protection
- Monitoring: Logging, metrics, alerting

### 2. Frontend Development

**Modern Frontend Practices:**
- Component-based architecture with proper separation of concerns
- State management (Redux, Context API, Vuex, Zustand)
- Responsive design and mobile-first approach
- Progressive Web Apps (PWA) implementation
- Accessibility (WCAG compliance) and SEO optimization
- Performance optimization (bundle size, lazy loading, code splitting)

**Frontend Security:**
- Input validation and sanitization on the client-side
- XSS protection through proper escaping and sanitization
- CSRF token implementation
- Secure handling of sensitive data in the browser
- Content Security Policy (CSP) implementation

**Frontend Performance:**
- Image optimization and lazy loading
- Code splitting and dynamic imports
- Caching strategies (HTTP caching, service workers)
- Bundle analysis and optimization
- Critical rendering path optimization

### 3. Backend Development

**API Development:**
- RESTful API design principles and best practices
- GraphQL implementation for flexible data fetching
- API versioning strategies
- Proper HTTP status codes and error handling
- Rate limiting and throttling implementation
- API documentation (OpenAPI/Swagger)

**Database Design & Management:**
- Schema design and normalization
- Index optimization for query performance
- Database migrations and version control
- Connection pooling and optimization
- Read replicas and sharding strategies
- Data validation and integrity constraints

**Backend Security:**
- Authentication (JWT, OAuth, Session-based)
- Authorization (RBAC, ABAC)
- Input validation and sanitization
- SQL injection prevention
- Mass assignment protection
- Secure session management

### 4. Testing Strategy

**Testing Pyramid Implementation:**
- Unit tests for individual functions and components
- Integration tests for API endpoints and database interactions
- End-to-end tests for critical user flows
- Contract testing for API interactions
- Performance and load testing
- Security testing and vulnerability scanning

**Test-Driven Development (TDD):**
- Writing tests before implementing features
- Behavior-driven development (BDD) approach
- Mocking and stubbing external dependencies
- Test coverage analysis and reporting
- Continuous testing in CI/CD pipelines

### 5. Deployment & DevOps

**CI/CD Pipeline:**
- Automated testing and code quality checks
- Multi-stage deployments (dev, staging, production)
- Blue-green or canary deployment strategies
- Infrastructure as Code (IaC) with Terraform/CloudFormation
- Containerization with Docker
- Orchestration with Kubernetes

**Monitoring & Observability:**
- Application performance monitoring (APM)
- Infrastructure monitoring and alerting
- Log aggregation and analysis
- Distributed tracing
- Business metrics and analytics
- Health checks and automated recovery

## Development Workflow

### 1. Project Setup

When starting a new full-stack project:

1. **Choose appropriate technology stack** based on requirements
2. **Set up development environment** with proper tools and dependencies
3. **Configure version control** with proper branching strategy
4. **Establish coding standards** and linting rules
5. **Set up testing framework** and initial test suite
6. **Configure CI/CD pipeline** for automated deployment

### 2. Feature Development

For each feature implementation:

1. **Analyze requirements** and break down into technical tasks
2. **Design the architecture** for the feature components
3. **Implement backend API** with proper validation and error handling
4. **Develop database schema** and migration scripts
5. **Create frontend components** with proper state management
6. **Write comprehensive tests** for all components
7. **Perform integration testing** between frontend and backend
8. **Deploy to staging environment** for review
9. **Conduct user acceptance testing**
10. **Deploy to production** with proper monitoring

### 3. Code Review Process

Follow these guidelines for effective code reviews:

- **Security first:** Check for potential vulnerabilities
- **Performance considerations:** Look for optimization opportunities
- **Maintainability:** Ensure code is readable and well-documented
- **Testing:** Verify adequate test coverage
- **Architecture compliance:** Ensure code follows established patterns
- **Error handling:** Check for proper error handling and logging

## Security Best Practices

### 1. Authentication & Authorization

**Implementation:**
- Use industry-standard JWT tokens or OAuth 2.0
- Implement proper password hashing (bcrypt, Argon2)
- Enforce strong password policies
- Implement multi-factor authentication (MFA)
- Use secure session management

**Validation:**
- Validate and sanitize all user inputs
- Implement proper input sanitization
- Use parameterized queries to prevent SQL injection
- Implement proper output encoding to prevent XSS
- Validate file uploads and implement size limits

### 2. Data Protection

**Encryption:**
- Encrypt data in transit using HTTPS/TLS
- Encrypt sensitive data at rest
- Use proper key management practices
- Implement proper secrets management
- Regular security audits and penetration testing

**Access Control:**
- Implement role-based access control (RBAC)
- Use principle of least privilege
- Regular access reviews and cleanup
- Audit trail for sensitive operations
- Proper API rate limiting and throttling

## Performance Optimization

### 1. Frontend Optimization

**Rendering Performance:**
- Optimize component rendering with React.memo or similar
- Implement virtual scrolling for large lists
- Use proper state management to avoid unnecessary re-renders
- Optimize images and use appropriate formats (WebP, AVIF)
- Implement proper lazy loading strategies

**Network Optimization:**
- Implement HTTP caching strategies
- Use CDN for static assets
- Optimize API calls with proper pagination
- Implement request batching where appropriate
- Use compression (Gzip, Brotli) for responses

### 2. Backend Optimization

**Database Performance:**
- Optimize database queries with proper indexing
- Use connection pooling efficiently
- Implement proper pagination for large datasets
- Use database read replicas for read-heavy operations
- Consider caching strategies (Redis, Memcached)

**API Performance:**
- Implement proper API rate limiting
- Use efficient serialization/deserialization
- Optimize API response sizes
- Implement proper caching strategies
- Use async processing for time-consuming operations

## Error Handling & Logging

### 1. Error Handling Strategy

**Frontend Error Handling:**
- Implement global error boundaries
- Show user-friendly error messages
- Log errors for debugging purposes
- Implement retry mechanisms for failed requests
- Graceful degradation for unavailable services

**Backend Error Handling:**
- Use centralized error handling middleware
- Implement proper HTTP status codes
- Log errors with appropriate context
- Implement circuit breaker patterns
- Use structured error responses

### 2. Logging & Monitoring

**Structured Logging:**
- Use consistent log formats across services
- Include request IDs for traceability
- Log important business events
- Implement proper log levels (debug, info, warn, error)
- Secure sensitive information in logs

**Monitoring Metrics:**
- Application performance metrics
- Database query performance
- API response times and error rates
- Resource utilization (CPU, memory, disk)
- Business metrics and KPIs

## Deployment Best Practices

### 1. Environment Management

**Configuration Management:**
- Use environment-specific configuration files
- Implement proper secrets management
- Use feature flags for gradual rollouts
- Maintain consistent environments across stages
- Document environment-specific settings

**Database Migrations:**
- Use version-controlled migration scripts
- Implement rollback strategies
- Test migrations in staging before production
- Schedule migrations during maintenance windows
- Backup databases before migrations

### 2. Production Monitoring

**Health Checks:**
- Implement readiness and liveness probes
- Monitor application health continuously
- Set up automated alerts for critical issues
- Implement self-healing mechanisms
- Document incident response procedures

**Performance Monitoring:**
- Monitor API response times
- Track database query performance
- Monitor resource utilization
- Set up performance baselines
- Implement automated scaling based on metrics

## Example Implementation Patterns

### Frontend Component Structure (React)
```jsx
// components/UserProfile/UserProfile.jsx
import React, { useState, useEffect } from 'react';
import { getUserProfile } from '../../services/userService';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorBoundary from '../common/ErrorBoundary';

const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        setLoading(true);
        const userData = await getUserProfile(userId);
        setUser(userData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchUserProfile();
    }
  }, [userId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <div>Error: {error}</div>;

  return (
    <ErrorBoundary>
      <div className="user-profile">
        <h2>{user?.name}</h2>
        <p>{user?.email}</p>
      </div>
    </ErrorBoundary>
  );
};

export default UserProfile;
```

### Backend API Endpoint (Express.js)
```javascript
// routes/users.js
const express = require('express');
const { body, param, query } = require('express-validator');
const { auth, authorize } = require('../middleware/auth');
const UserController = require('../controllers/UserController');

const router = express.Router();

// Validation middleware
const validateUserId = [
  param('id').isMongoId().withMessage('Invalid user ID format')
];

const validateUserUpdate = [
  body('email').optional().isEmail().normalizeEmail(),
  body('firstName').optional().trim().isLength({ min: 1, max: 50 }),
  body('lastName').optional().trim().isLength({ min: 1, max: 50 })
];

// GET /api/users/:id - Get user by ID (authenticated users)
router.get('/:id', validateUserId, auth, UserController.getById);

// PUT /api/users/:id - Update user (authenticated users)
router.put('/:id', validateUserId, validateUserUpdate, auth, UserController.update);

// DELETE /api/users/:id - Delete user (admin only)
router.delete('/:id', validateUserId, auth, authorize('admin'), UserController.delete);

module.exports = router;
```

### Database Model (Mongoose)
```javascript
// models/User.js
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [8, 'Password must be at least 8 characters']
  },
  firstName: {
    type: String,
    required: [true, 'First name is required'],
    trim: true
  },
  lastName: {
    type: String,
    required: [true, 'Last name is required'],
    trim: true
  },
  role: {
    type: String,
    enum: ['user', 'admin', 'moderator'],
    default: 'user'
  },
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true,
  toJSON: {
    transform: function(doc, ret) {
      delete ret.password;
      return ret;
    }
  }
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();

  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
```

## When to Use This Skill

Use this skill when working on:
- Full-stack application development projects
- Architecture design and technical decision making
- Security implementation and vulnerability assessment
- Performance optimization and scaling challenges
- Testing strategy and implementation
- Deployment and DevOps tasks
- Code review and quality assurance
- Troubleshooting production issues
- Technology stack evaluation and selection

## Resources

This skill includes comprehensive resources for full-stack development:

### scripts/
Helper scripts for common full-stack development tasks:
- Environment setup and configuration
- Database migration utilities
- Deployment automation scripts
- Performance testing tools
- Security scanning utilities

### references/
Detailed documentation and reference materials:
- API design guidelines and best practices
- Security implementation patterns
- Performance optimization techniques
- Architecture decision records
- Code style and formatting guidelines

### assets/
Template files and boilerplate code:
- Project starter templates for different tech stacks
- Component boilerplate files
- Configuration file templates
- Testing framework setup files
- Deployment configuration examples
