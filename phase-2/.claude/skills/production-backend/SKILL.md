---
name: production-backend
description: Comprehensive production-ready backend development with Node.js, Python, Java, Go, and modern architecture patterns. Use when Claude needs to work with production backend applications for creating REST APIs, implementing microservices architecture, setting up database connections, implementing authentication and authorization, following security best practices, implementing caching strategies, setting up monitoring and observability, or any other production backend development tasks.
---

# Production Backend Development

## Overview

This skill provides comprehensive guidance for building production-ready backend applications using modern technologies and best practices. It covers API development, database design, security implementation, performance optimization, monitoring, and deployment strategies. The skill ensures applications are scalable, maintainable, secure, and follow industry standards.

## Core Capabilities

### 1. API Development and Design
- RESTful API design principles and best practices
- GraphQL implementation and schema design
- API versioning strategies
- Rate limiting and throttling implementation
- API documentation with OpenAPI/Swagger

### 2. Database Management
- SQL and NoSQL database design patterns
- ORM/ODM implementation and optimization
- Database migration strategies
- Connection pooling and optimization
- Data modeling and normalization

### 3. Authentication and Authorization
- JWT token implementation
- OAuth 2.0 and OpenID Connect integration
- Role-based access control (RBAC)
- Session management
- Password hashing and security

### 4. Security Implementation
- Input validation and sanitization
- SQL injection prevention
- Cross-site scripting (XSS) protection
- API security headers
- HTTPS and TLS configuration

### 5. Microservices Architecture
- Service decomposition strategies
- API gateway implementation
- Service discovery patterns
- Inter-service communication
- Circuit breaker and retry patterns

### 6. Performance Optimization
- Caching strategies (Redis, Memcached)
- Database query optimization
- Load balancing implementation
- CDN configuration
- Response compression

## Project Structure

### Recommended Backend Structure
```
production-backend/
├── apps/
│   └── api/
│       ├── src/
│       │   ├── controllers/
│       │   ├── routes/
│       │   ├── middleware/
│       │   ├── models/
│       │   ├── services/
│       │   ├── utils/
│       │   └── config/
│       ├── tests/
│       │   ├── unit/
│       │   ├── integration/
│       │   └── e2e/
│       ├── docs/
│       ├── .env.example
│       ├── package.json
│       └── Dockerfile
├── packages/
│   ├── database/
│   ├── auth/
│   ├── common/
│   └── types/
├── infrastructure/
│   ├── docker/
│   ├── k8s/
│   └── terraform/
├── specs/
├── scripts/
├── .github/
│   └── workflows/
├── .specify/
└── tooling/
    ├── eslint/
    ├── prettier/
    └── typescript/
```

## Backend Implementation Patterns

### 1. Express.js API Structure
```javascript
// src/app.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();

// Security middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Routes
app.use('/api/users', require('./routes/users'));
app.use('/api/posts', require('./routes/posts'));

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

module.exports = app;
```

### 2. Database Model with Mongoose (Node.js) / SQLAlchemy (Python)
```javascript
// models/User.js (Node.js with Mongoose)
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true,
    minlength: 8
  },
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
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
  timestamps: true
});

// Password hashing middleware
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
```

### 3. Authentication Middleware
```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');
const User = require('../models/User');

const auth = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({ error: 'Access denied. No token provided.' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.userId).select('-password');

    if (!user || !user.isActive) {
      return res.status(401).json({ error: 'Invalid token.' });
    }

    req.user = user;
    next();
  } catch (error) {
    res.status(400).json({ error: 'Invalid token.' });
  }
};

module.exports = auth;
```

### 4. API Route with Validation
```javascript
// routes/users.js
const express = require('express');
const { body, validationResult } = require('express-validator');
const auth = require('../middleware/auth');
const User = require('../models/User');

const router = express.Router();

// GET /api/users/profile - Get current user profile
router.get('/profile', auth, async (req, res) => {
  res.json({
    id: req.user.id,
    email: req.user.email,
    firstName: req.user.firstName,
    lastName: req.user.lastName,
    role: req.user.role
  });
});

// POST /api/users/register - Register new user
router.post('/register', [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }),
  body('firstName').trim().isLength({ min: 1, max: 50 }),
  body('lastName').trim().isLength({ min: 1, max: 50 })
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    const { email, password, firstName, lastName } = req.body;

    // Check if user exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ error: 'User already exists' });
    }

    // Create new user
    const user = new User({ email, password, firstName, lastName });
    await user.save();

    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id },
      process.env.JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.status(201).json({
      token,
      user: {
        id: user._id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
```

## Security Implementation

### 1. Input Validation and Sanitization
```javascript
// middleware/validation.js
const validator = require('validator');
const sanitize = require('mongo-sanitize');

const validateAndSanitize = (req, res, next) => {
  // Sanitize input to prevent NoSQL injection
  req.body = sanitize(req.body);
  req.query = sanitize(req.query);
  req.params = sanitize(req.params);

  // Validate and sanitize each field
  if (req.body.email) {
    req.body.email = validator.normalizeEmail(req.body.email);
  }

  if (req.body.url) {
    req.body.url = validator.normalizeURL(req.body.url);
  }

  next();
};

module.exports = validateAndSanitize;
```

### 2. Helmet Security Headers
```javascript
// app.js
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
  frameguard: {
    action: 'deny',
  },
}));
```

## Performance Optimization

### 1. Redis Caching Implementation
```javascript
// services/cache.js
const redis = require('redis');

class CacheService {
  constructor() {
    this.client = redis.createClient({
      host: process.env.REDIS_HOST || 'localhost',
      port: process.env.REDIS_PORT || 6379,
    });

    this.client.on('error', (err) => {
      console.error('Redis Client Error', err);
    });

    this.client.connect();
  }

  async get(key) {
    try {
      const value = await this.client.get(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  }

  async set(key, value, expiration = 3600) {
    try {
      await this.client.setEx(key, expiration, JSON.stringify(value));
    } catch (error) {
      console.error('Cache set error:', error);
    }
  }

  async delete(key) {
    try {
      await this.client.del(key);
    } catch (error) {
      console.error('Cache delete error:', error);
    }
  }
}

module.exports = new CacheService();
```

### 2. Database Query Optimization
```javascript
// services/userService.js
const User = require('../models/User');

class UserService {
  // Efficient query with projection and indexing
  async getUserById(userId) {
    return await User.findById(userId)
      .select('-password -__v') // Exclude sensitive fields
      .lean(); // Return plain JS object instead of Mongoose doc
  }

  // Paginated query
  async getUsers(page = 1, limit = 10) {
    const skip = (page - 1) * limit;

    const users = await User.find({ isActive: true })
      .select('email firstName lastName role createdAt')
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .lean();

    const total = await User.countDocuments({ isActive: true });

    return {
      users,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    };
  }

  // Aggregation for complex queries
  async getUserStats() {
    return await User.aggregate([
      {
        $group: {
          _id: '$role',
          count: { $sum: 1 },
          activeCount: {
            $sum: { $cond: [{ $eq: ['$isActive', true] }, 1, 0] }
          }
        }
      }
    ]);
  }
}

module.exports = new UserService();
```

## Microservices Architecture

### 1. Service Communication Pattern
```javascript
// services/apiClient.js
const axios = require('axios');

class APIClient {
  constructor(baseURL, serviceName) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'User-Agent': `Service-${serviceName}/1.0`,
        'Content-Type': 'application/json'
      }
    });

    // Add request interceptor for authentication
    this.client.interceptors.request.use(
      (config) => {
        config.headers['Authorization'] = `Bearer ${process.env.SERVICE_TOKEN}`;
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error(`API call failed to ${error.config?.baseURL || 'unknown'}:`, error.message);
        return Promise.reject(error);
      }
    );
  }

  async get(path, options = {}) {
    try {
      const response = await this.client.get(path, options);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  async post(path, data, options = {}) {
    try {
      const response = await this.client.post(path, data, options);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  handleError(error) {
    if (error.response) {
      // Server responded with error status
      return new Error(`API Error: ${error.response.status} - ${error.response.data?.message || 'Unknown error'}`);
    } else if (error.request) {
      // Request was made but no response received
      return new Error('Network Error: No response received');
    } else {
      // Something else happened
      return new Error(`Request Error: ${error.message}`);
    }
  }
}

module.exports = APIClient;
```

### 2. Message Queue Pattern (using Bull for Node.js)
```javascript
// services/queue.js
const Queue = require('bull');
const EmailService = require('./emailService');

// Create queue
const emailQueue = new Queue('email sending', process.env.REDIS_URL);

// Process jobs
emailQueue.process('sendWelcomeEmail', async (job) => {
  const { userId, email, name } = job.data;

  try {
    await EmailService.sendWelcomeEmail(email, name);
    console.log(`Welcome email sent to ${email}`);
  } catch (error) {
    console.error(`Failed to send welcome email to ${email}:`, error);
    throw error; // This will retry the job
  }
});

// Add job to queue
const addWelcomeEmailJob = async (userData) => {
  return await emailQueue.add('sendWelcomeEmail', userData, {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000
    },
    removeOnComplete: true,
    removeOnFail: 100
  });
};

module.exports = {
  emailQueue,
  addWelcomeEmailJob
};
```

## Monitoring and Observability

### 1. Logging Implementation
```javascript
// utils/logger.js
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'production-backend' },
  transports: [
    // Write all logs with level 'error' and below to error.log
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error'
    }),
    // Write all logs with level 'info' and below to combined.log
    new winston.transports.File({
      filename: 'logs/combined.log'
    })
  ]
});

// If not in production, also log to console
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  }));
}

module.exports = logger;
```

### 2. Health Check Endpoint
```javascript
// routes/health.js
const express = require('express');
const mongoose = require('mongoose');
const redis = require('redis');

const router = express.Router();

router.get('/health', async (req, res) => {
  try {
    // Check database connection
    const dbStatus = mongoose.connection.readyState === 1 ? 'connected' : 'disconnected';

    // Check Redis connection (if used)
    let redisStatus = 'disabled';
    if (process.env.REDIS_URL) {
      try {
        await redis.ping();
        redisStatus = 'connected';
      } catch (error) {
        redisStatus = 'disconnected';
      }
    }

    const healthCheck = {
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      checks: {
        database: dbStatus,
        redis: redisStatus,
        memory: {
          used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + ' MB',
          total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024) + ' MB'
        },
        cpu: process.cpuUsage()
      }
    };

    // If any check failed, return 503
    if (dbStatus === 'disconnected' || redisStatus === 'disconnected') {
      return res.status(503).json(healthCheck);
    }

    res.status(200).json(healthCheck);
  } catch (error) {
    res.status(503).json({
      status: 'error',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

module.exports = router;
```

## Deployment Configuration

### 1. Dockerfile for Production
```dockerfile
# Use official Node.js runtime as parent image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Change ownership of the app directory
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Run the application
CMD ["npm", "start"]
```

### 2. Environment Configuration
```bash
# .env.example
NODE_ENV=production
PORT=3000

# Database
DATABASE_URL=mongodb://localhost:27017/myapp
DATABASE_POOL_SIZE=20

# JWT
JWT_SECRET=your-super-secret-jwt-key-here
JWT_EXPIRES_IN=7d

# Redis
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=your-redis-password

# API Keys
SENDGRID_API_KEY=your-sendgrid-api-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# Security
CORS_ORIGIN=https://yourdomain.com
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX=100

# Logging
LOG_LEVEL=info
LOG_PRETTY_PRINT=false
```

## Quality Assurance Framework

### 1. ESLint Configuration for Backend
```javascript
// tooling/eslint/backend.js
module.exports = {
  env: {
    node: true,
    es2021: true,
    jest: true,
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: [
    '@typescript-eslint',
    'import',
    'security',
    'jest',
  ],
  rules: {
    'no-console': 'warn',
    'no-process-env': 'warn',
    'jest/expect-expect': 'off',
    'security/detect-object-injection': 'off',
    'security/detect-non-literal-fs-filename': 'off',
    'security/detect-unsafe-regex': 'error',
    'security/detect-buffer-noassert': 'error',
    'security/detect-child-process': 'error',
    'security/detect-disable-mustache-escape': 'error',
    'security/detect-eval-with-expression': 'error',
    'security/detect-new-buffer': 'error',
    'security/detect-no-csrf-before-method-override': 'error',
    'security/detect-non-literal-regexp': 'error',
    'security/detect-possible-timing-attacks': 'error',
    'security/detect-pseudoRandomBytes': 'error',
    'security/detect-unsafe-regex': 'error',
    'import/order': [
      'error',
      {
        groups: [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          'index',
        ],
        pathGroups: [
          {
            pattern: '@/**',
            group: 'internal',
          },
        ],
        pathGroupsExcludedImportTypes: ['builtin'],
        alphabetize: {
          order: 'asc',
          caseInsensitive: true,
        },
      },
    ],
  },
  overrides: [
    {
      files: ['**/*.test.js', '**/*.spec.js'],
      env: {
        jest: true,
      },
      rules: {
        'no-console': 'off',
      },
    },
  ],
};
```

### 2. Testing Framework Implementation
```javascript
// tests/unit/userService.test.js
const { MongoMemoryServer } = require('mongodb-memory-server');
const mongoose = require('mongoose');
const User = require('../../src/models/User');
const UserService = require('../../src/services/userService');

describe('UserService', () => {
  let mongoServer;

  beforeAll(async () => {
    mongoServer = await MongoMemoryServer.create();
    await mongoose.connect(mongoServer.getUri());
  });

  afterAll(async () => {
    await mongoose.disconnect();
    await mongoServer.stop();
  });

  beforeEach(async () => {
    await User.deleteMany({});
  });

  describe('getUserById', () => {
    it('should return user by ID', async () => {
      const user = new User({
        email: 'test@example.com',
        password: 'hashedPassword',
        firstName: 'John',
        lastName: 'Doe'
      });
      await user.save();

      const result = await UserService.getUserById(user._id);

      expect(result).toBeDefined();
      expect(result.email).toBe('test@example.com');
      expect(result.firstName).toBe('John');
      expect(result.lastName).toBe('Doe');
      expect(result.password).toBeUndefined(); // Should be excluded
    });

    it('should return null for non-existent user', async () => {
      const result = await UserService.getUserById('507f1f77bcf86cd799439011');

      expect(result).toBeNull();
    });
  });

  describe('getUsers', () => {
    it('should return paginated users', async () => {
      // Create test users
      await User.create([
        { email: 'user1@example.com', password: 'pass', firstName: 'User', lastName: 'One' },
        { email: 'user2@example.com', password: 'pass', firstName: 'User', lastName: 'Two' },
        { email: 'user3@example.com', password: 'pass', firstName: 'User', lastName: 'Three' }
      ]);

      const result = await UserService.getUsers(1, 2);

      expect(result.users).toHaveLength(2);
      expect(result.pagination.total).toBe(3);
      expect(result.pagination.pages).toBe(2);
    });
  });
});
```

## Development Workflow

### 1. Project Initialization
1. Set up project structure with proper separation of concerns
2. Configure environment variables and secrets management
3. Set up database connections and ORM/ODM
4. Configure authentication and authorization
5. Set up testing framework (unit, integration, e2e)
6. Configure CI/CD pipeline

### 2. API Development Process
1. Design API endpoints following REST principles
2. Implement input validation and sanitization
3. Write unit tests for each endpoint
4. Implement security measures (rate limiting, authentication)
5. Add logging and monitoring
6. Document API with OpenAPI specification

### 3. Code Review Checklist
- [ ] Input validation implemented for all endpoints
- [ ] Authentication and authorization applied correctly
- [ ] Database queries are optimized and use proper indexing
- [ ] Error handling covers edge cases
- [ ] Security best practices followed (no secrets in code, proper sanitization)
- [ ] Tests cover happy path and error scenarios
- [ ] Performance considerations addressed (caching, pagination)

## Resources

### references/
- `api_design_patterns.md` - RESTful API design and best practices
- `database_optimization.md` - Database design and query optimization techniques
- `security_best_practices.md` - Backend security implementation guidelines
- `microservices_patterns.md` - Microservices architecture patterns
- `testing_strategies.md` - Backend testing approaches and frameworks
- `deployment_strategies.md` - Production deployment patterns

### assets/
- `api_templates/` - API route and controller boilerplates
- `model_templates/` - Database model templates
- `middleware_templates/` - Common middleware implementations
- `configuration_templates/` - Environment and configuration files
- `test_templates/` - Test file templates and utilities
