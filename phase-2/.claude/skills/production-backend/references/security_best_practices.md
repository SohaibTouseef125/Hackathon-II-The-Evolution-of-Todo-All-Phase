# Backend Security Implementation Guidelines

## Authentication and Authorization

### JWT Implementation Best Practices
```javascript
// Secure JWT generation
const jwt = require('jsonwebtoken');

// Use strong secret key
const generateToken = (payload) => {
  return jwt.sign(payload, process.env.JWT_SECRET, {
    expiresIn: '15m',  // Short-lived access token
    issuer: 'your-app',
    audience: 'your-app-users'
  });
};

// Refresh token pattern
const generateRefreshToken = (userId) => {
  const refreshToken = jwt.sign(
    { userId, type: 'refresh' },
    process.env.REFRESH_TOKEN_SECRET,
    { expiresIn: '7d' }
  );

  // Store refresh token in database for invalidation
  await RefreshToken.create({
    token: refreshToken,
    userId,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  });

  return refreshToken;
};
```

### Session Management
```javascript
// Secure session configuration
const session = require('express-session');
const MongoStore = require('connect-mongo');

app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  store: MongoStore.create({
    mongoUrl: process.env.MONGODB_URI
  }),
  cookie: {
    secure: process.env.NODE_ENV === 'production', // HTTPS only in production
    httpOnly: true, // Prevent XSS
    maxAge: 24 * 60 * 60 * 1000, // 24 hours
    sameSite: 'strict' // CSRF protection
  }
}));
```

### OAuth 2.0 and OpenID Connect
```javascript
// OAuth 2.0 implementation with Passport.js
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL: "/auth/google/callback",
  scope: ['profile', 'email']
}, async (accessToken, refreshToken, profile, done) => {
  try {
    // Verify the user's identity
    const user = await User.findOne({ googleId: profile.id });
    if (user) return done(null, user);

    // Create new user if doesn't exist
    const newUser = await User.create({
      googleId: profile.id,
      email: profile.emails[0].value,
      name: profile.displayName
    });

    return done(null, newUser);
  } catch (error) {
    return done(error, null);
  }
}));
```

## Input Validation and Sanitization

### Request Validation
```javascript
// Using express-validator for input validation
const { body, validationResult } = require('express-validator');

const validateUserRegistration = [
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Must be a valid email')
    .bail()
    .custom(async (value) => {
      const existingUser = await User.findOne({ email: value });
      if (existingUser) {
        throw new Error('Email already in use');
      }
    }),

  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters long')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password must contain at least one uppercase, lowercase, and number'),

  body('firstName')
    .trim()
    .isLength({ max: 50 })
    .withMessage('First name must be less than 50 characters'),

  body('lastName')
    .trim()
    .isLength({ max: 50 })
    .withMessage('Last name must be less than 50 characters')
];

const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      errors: errors.array()
    });
  }
  next();
};

// Usage in route
app.post('/api/users/register',
  validateUserRegistration,
  handleValidationErrors,
  registerController
);
```

### NoSQL Injection Prevention
```javascript
// Safe MongoDB queries
const mongoSanitize = require('express-mongo-sanitize');

// Middleware to sanitize MongoDB queries
app.use(mongoSanitize({
  replaceWith: '_'  // Replace dangerous characters with underscore
}));

// Manual sanitization
const sanitizeQuery = (query) => {
  // Remove any keys that start with $ or contain .
  const sanitized = {};
  for (const [key, value] of Object.entries(query)) {
    if (key.startsWith('$') || key.includes('.')) {
      continue; // Skip potentially dangerous keys
    }
    sanitized[key] = value;
  }
  return sanitized;
};

// Safe query construction
const findUserSafely = async (query) => {
  const sanitizedQuery = sanitizeQuery(query);
  return await User.findOne(sanitizedQuery);
};
```

## SQL Injection Prevention

### Using Parameterized Queries
```javascript
// Safe query with parameterized statements
const getUserById = async (userId) => {
  // Using parameterized query - safe
  const result = await db.query(
    'SELECT * FROM users WHERE id = $1',
    [userId]
  );
  return result.rows[0];
};

// Using an ORM safely
const getUserByEmail = async (email) => {
  // ORM automatically parameterizes - safe
  return await User.findOne({
    where: {
      email: email  // Safe from SQL injection
    }
  });
};

// Avoid string concatenation in queries
// NEVER do this:
// const query = `SELECT * FROM users WHERE email = '${email}'`;
```

## Cross-Site Scripting (XSS) Prevention

### Output Encoding
```javascript
// Server-side XSS prevention
const xss = require('xss');

const sanitizeOutput = (input) => {
  // Sanitize HTML content
  return xss(input, {
    whiteList: {
      p: [],
      br: [],
      strong: [],
      em: [],
      u: [],
      ol: [],
      ul: [],
      li: []
    }
  });
};

// Safe template rendering
app.get('/profile/:id', async (req, res) => {
  const user = await User.findById(req.params.id);

  // Sanitize any user-generated content before sending
  const safeUser = {
    ...user,
    bio: sanitizeOutput(user.bio || ''),
    profile: sanitizeOutput(user.profile || '')
  };

  res.json(safeUser);
});
```

### Content Security Policy (CSP)
```javascript
// Implementing CSP headers
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
    scriptSrc: ["'self'"],
    imgSrc: ["'self'", "data:", "https:"],
    fontSrc: ["'self'", "https://fonts.gstatic.com"],
    connectSrc: ["'self'", "https://api.example.com"],
    objectSrc: ["'none'"],
    frameSrc: ["'none'"],
    baseUri: ["'self'"],
    formAction: ["'self'"],
    frameAncestors: ["'none'"]
  }
}));
```

## Cross-Site Request Forgery (CSRF) Protection

### CSRF Token Implementation
```javascript
// CSRF protection with csurf
const csrf = require('csurf');

app.use(csrf());

// Middleware to provide CSRF token to frontend
app.use((req, res, next) => {
  res.locals.csrfToken = req.csrfToken();
  next();
});

// Frontend template should include token
// <input type="hidden" name="_csrf" value="{{csrfToken}}">

// Or API header approach
app.use((req, res, next) => {
  // Allow requests with proper header
  if (req.headers['x-csrf-token']) {
    req.csrfToken = () => req.headers['x-csrf-token'];
  }
  next();
});
```

## Rate Limiting and DDoS Protection

### API Rate Limiting
```javascript
const rateLimit = require('express-rate-limit');

// General rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
});

app.use('/api/', limiter);

// Specific route rate limiting
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Limit each IP to 5 login requests per windowMs
  message: 'Too many login attempts, please try again later.',
  skipSuccessfulRequests: true // Don't count successful logins
});

app.post('/api/auth/login', authLimiter, loginController);

// Custom rate limiting by user
const userRateLimit = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: (req, res) => {
    // Different limits based on user role
    if (req.user && req.user.role === 'premium') {
      return 100; // Premium users get higher limits
    }
    return 10; // Regular users get lower limits
  }
});
```

## Data Encryption and Security

### Password Hashing
```javascript
const bcrypt = require('bcrypt');

// Secure password hashing
const hashPassword = async (password) => {
  // Use a high salt rounds for security (but consider performance)
  const saltRounds = 12;
  return await bcrypt.hash(password, saltRounds);
};

// Secure password verification
const verifyPassword = async (password, hashedPassword) => {
  return await bcrypt.compare(password, hashedPassword);
};

// User model with secure password handling
const UserSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true }
});

UserSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();

  try {
    // Hash password before saving
    this.password = await hashPassword(this.password);
    next();
  } catch (error) {
    next(error);
  }
});
```

### Data Encryption
```javascript
const crypto = require('crypto');

// Encrypt sensitive data
const encryptData = (text, key) => {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipher('aes-256-cbc', key);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return iv.toString('hex') + ':' + encrypted;
};

// Decrypt sensitive data
const decryptData = (encryptedText, key) => {
  const [ivHex, encrypted] = encryptedText.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const decipher = crypto.createDecipher('aes-256-cbc', key);
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
};

// Environment-specific encryption keys
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || crypto.randomBytes(32);
```

## API Security Headers

### Security Headers Implementation
```javascript
const helmet = require('helmet');

app.use(helmet({
  // Helps prevent cross-site scripting (XSS) attacks
  xssFilter: true,

  // Adds the X-Frame-Options header to help prevent clickjacking
  frameguard: {
    action: 'deny'
  },

  // Adds the Strict-Transport-Security header
  hsts: {
    maxAge: 31536000, // 1 year in seconds
    includeSubDomains: true,
    preload: true
  },

  // Adds the X-Content-Type-Options header
  noSniff: true,

  // Redirects HTTP requests to HTTPS
  forceHttps: {
    trustProtoHeader: true // Trust the X-Forwarded-Proto header
  }
}));

// Additional security headers
app.use((req, res, next) => {
  // Prevent MIME-type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // Prevent loading content from other domains
  res.setHeader('X-Frame-Options', 'DENY');

  // Enable browser's XSS protection
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Limit referrer information
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  next();
});
```

## File Upload Security

### Secure File Upload Handling
```javascript
const multer = require('multer');
const path = require('path');

// Configure secure file upload
const fileUpload = multer({
  dest: 'uploads/',
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB limit
    files: 1 // Only allow one file at a time
  },
  fileFilter: (req, file, cb) => {
    // Allow only specific file types
    const allowedTypes = /jpeg|jpg|png|pdf|doc|docx/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);

    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only images and documents are allowed.'));
    }
  }
});

// Secure file upload endpoint
app.post('/api/upload', auth, fileUpload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Validate file after upload
    const fs = require('fs');
    const fileType = require('file-type');

    const buffer = await fs.promises.readFile(req.file.path);
    const type = await fileType.fromBuffer(buffer);

    if (!type || !['image/jpeg', 'image/png', 'application/pdf'].includes(type.mime)) {
      // Remove uploaded file
      await fs.promises.unlink(req.file.path);
      return res.status(400).json({ error: 'Invalid file type after validation' });
    }

    // Generate secure filename
    const secureFilename = `${Date.now()}-${Math.random().toString(36).substring(2, 15)}${path.extname(req.file.originalname)}`;
    const destinationPath = path.join('uploads', secureFilename);

    // Move to final location
    await fs.promises.rename(req.file.path, destinationPath);

    res.json({
      message: 'File uploaded successfully',
      filename: secureFilename
    });
  } catch (error) {
    res.status(500).json({ error: 'Upload failed' });
  }
});
```

## Security Monitoring and Logging

### Security Event Logging
```javascript
const logger = require('./utils/logger'); // Your logger implementation

// Log security events
const logSecurityEvent = (type, req, details = {}) => {
  logger.warn('SECURITY_EVENT', {
    type,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
    url: req.originalUrl,
    method: req.method,
    userId: req.user?.id || 'unauthenticated',
    timestamp: new Date().toISOString(),
    details
  });
};

// Security middleware for logging
const securityLogger = (req, res, next) => {
  // Log authentication failures
  res.on('finish', () => {
    if (res.statusCode === 401 || res.statusCode === 403) {
      logSecurityEvent('AUTH_FAILURE', req, {
        statusCode: res.statusCode
      });
    }
  });

  next();
};

app.use(securityLogger);

// Monitor for suspicious activities
const suspiciousActivityMonitor = {
  failedLoginAttempts: new Map(),

  checkFailedLogin(ip) {
    const attempts = this.failedLoginAttempts.get(ip) || 0;
    if (attempts >= 5) {
      logSecurityEvent('BRUTE_FORCE_ATTEMPT', { ip });
      return true; // Block further attempts
    }
    return false;
  },

  recordFailedLogin(ip) {
    const attempts = this.failedLoginAttempts.get(ip) || 0;
    this.failedLoginAttempts.set(ip, attempts + 1);

    // Reset after 15 minutes
    setTimeout(() => {
      if (this.failedLoginAttempts.get(ip) === attempts + 1) {
        this.failedLoginAttempts.delete(ip);
      }
    }, 15 * 60 * 1000);
  }
};
```

## Environment and Configuration Security

### Secure Environment Management
```javascript
// Validate required environment variables
const requiredEnvVars = [
  'JWT_SECRET',
  'DATABASE_URL',
  'ENCRYPTION_KEY',
  'SESSION_SECRET'
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}

// Never log sensitive information
const sanitizeForLogging = (obj) => {
  const sanitized = { ...obj };
  const sensitiveFields = ['password', 'token', 'secret', 'key', 'auth'];

  for (const field of sensitiveFields) {
    if (sanitized[field]) {
      sanitized[field] = '[REDACTED]';
    }
  }

  return sanitized;
};
```

This security guide provides comprehensive backend security implementation patterns for production applications, covering authentication, input validation, data protection, and monitoring best practices.