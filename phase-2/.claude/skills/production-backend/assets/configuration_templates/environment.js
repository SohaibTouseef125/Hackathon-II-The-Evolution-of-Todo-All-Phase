// config/environment.js
const path = require('path');

// Load environment variables from .env file
require('dotenv').config({ path: path.resolve(process.cwd(), '.env') });

// Validate required environment variables
const requiredEnvVars = [
  'NODE_ENV',
  'PORT',
  'JWT_SECRET',
  'DATABASE_URL',
  'REDIS_URL'
];

const missingEnvVars = requiredEnvVars.filter(envVar => !process.env[envVar]);
if (missingEnvVars.length > 0) {
  throw new Error(`Missing required environment variables: ${missingEnvVars.join(', ')}`);
}

const config = {
  // Environment
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT) || 3000,

  // Database
  database: {
    url: process.env.DATABASE_URL,
    options: {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      maxPoolSize: parseInt(process.env.DB_POOL_SIZE) || 10,
      serverSelectionTimeoutMS: 5000,
      socketTimeoutMS: 45000,
    }
  },

  // JWT
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '1d',
    refreshSecret: process.env.JWT_REFRESH_SECRET || process.env.JWT_SECRET + '_refresh',
    refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d'
  },

  // Redis
  redis: {
    url: process.env.REDIS_URL,
    options: {
      retryDelayOnFailover: 100,
      maxRetriesPerRequest: 3,
      enableReadyCheck: true
    }
  },

  // CORS
  cors: {
    origin: process.env.CORS_ORIGIN ? process.env.CORS_ORIGIN.split(',') : ['http://localhost:3000'],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Origin', 'X-Requested-With', 'Content-Type', 'Accept', 'Authorization']
  },

  // Rate Limiting
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000, // 15 minutes
    max: parseInt(process.env.RATE_LIMIT_MAX) || 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    format: process.env.LOG_FORMAT || 'combined',
    prettyPrint: process.env.NODE_ENV === 'development' || process.env.LOG_PRETTY_PRINT === 'true'
  },

  // Security
  security: {
    helmet: {
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          scriptSrc: ["'self'"],
          imgSrc: ["'self'", "data:", "https:"],
          fontSrc: ["'self'", "https://fonts.gstatic.com"],
          connectSrc: ["'self'", "https://api.example.com"],
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
    },
    cors: {
      origin: process.env.CORS_ORIGIN ? process.env.CORS_ORIGIN.split(',') : ['http://localhost:3000'],
      credentials: true,
    }
  },

  // API Keys and External Services
  services: {
    email: {
      provider: process.env.EMAIL_PROVIDER || 'smtp',
      apiKey: process.env.SENDGRID_API_KEY,
      from: process.env.EMAIL_FROM || 'noreply@yourdomain.com'
    },
    payment: {
      provider: process.env.PAYMENT_PROVIDER || 'stripe',
      publicKey: process.env.STRIPE_PUBLIC_KEY,
      secretKey: process.env.STRIPE_SECRET_KEY
    }
  },

  // File Upload
  upload: {
    maxFileSize: parseInt(process.env.MAX_FILE_SIZE) || 5 * 1024 * 1024, // 5MB
    allowedMimeTypes: [
      'image/jpeg',
      'image/png',
      'image/gif',
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ],
    uploadDir: process.env.UPLOAD_DIR || './uploads'
  },

  // Cache
  cache: {
    ttl: parseInt(process.env.CACHE_TTL) || 3600, // 1 hour
    prefix: process.env.CACHE_PREFIX || 'app:'
  },

  // External APIs
  external: {
    timeout: parseInt(process.env.EXTERNAL_API_TIMEOUT) || 10000, // 10 seconds
    retries: parseInt(process.env.EXTERNAL_API_RETRIES) || 3
  }
};

// Additional environment-specific configurations
if (config.env === 'development') {
  config.database.options = {
    ...config.database.options,
    useCreateIndex: true,
    useFindAndModify: false,
  };

  // Development-specific logging
  config.logging.level = 'debug';
}

if (config.env === 'production') {
  // Production-specific security enhancements
  config.security.helmet = {
    ...config.security.helmet,
    forceHttps: true,
    noSniff: true,
    xssFilter: true,
  };

  // Production-specific performance settings
  config.database.options.maxPoolSize = 20;
}

if (config.env === 'test') {
  // Test-specific configurations
  config.port = 3001;
  config.database.url = process.env.TEST_DATABASE_URL || config.database.url;
  config.logging.level = 'error';
}

module.exports = config;