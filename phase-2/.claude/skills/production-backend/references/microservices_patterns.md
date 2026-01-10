# Microservices Architecture Patterns

## Service Decomposition Strategies

### Domain-Driven Design (DDD)
- **Bounded Contexts**: Organize services around business domains
- **Context Maps**: Define relationships between different bounded contexts
- **Ubiquitous Language**: Use consistent terminology within each context

### Service Sizing Guidelines
- **Single Responsibility**: Each service should have one clear purpose
- **Team Size**: Follow Conway's Law - team size should match service complexity
- **Data Ownership**: Each service should own its data and provide an API for access

### Decomposition Patterns
1. **By Business Capability**: Group services by business functions
2. **By Subdomain**: Based on strategic domain-driven design
3. **By Common Closure**: Group elements that change together
4. **By Transaction Boundary**: Separate services by transactional needs

## API Gateway Implementation

### Gateway Responsibilities
```javascript
// Example API Gateway with Express
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// Authentication middleware for the gateway
app.use('/api', authenticateRequest);

// Rate limiting at the gateway level
app.use('/api', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
}));

// Route to user service
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3000',
  changeOrigin: true,
  pathRewrite: {
    '^/api/users': '/users'
  }
}));

// Route to order service
app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3000',
  changeOrigin: true,
  pathRewrite: {
    '^/api/orders': '/orders'
  }
}));

// Request/response transformation
app.use('/api/products', createProxyMiddleware({
  target: 'http://product-service:3000',
  changeOrigin: true,
  onProxyReq: (proxyReq, req, res) => {
    // Add headers or modify request
    proxyReq.setHeader('X-Forwarded-For', req.connection.remoteAddress);
  },
  onProxyRes: (proxyRes, req, res) => {
    // Modify response if needed
    proxyRes.headers['X-Powered-By'] = 'API-Gateway';
  }
}));
```

### Gateway Security
```javascript
// Gateway security patterns
const jwt = require('jsonwebtoken');

const authenticateRequest = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

// API Key validation
const validateApiKey = (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  if (!apiKey || !isValidApiKey(apiKey)) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  next();
};
```

## Service Discovery Patterns

### Client-Side Discovery
```javascript
// Service discovery with Consul
const consul = require('consul')();

class ServiceDiscovery {
  constructor() {
    this.serviceCache = new Map();
    this.refreshInterval = 30000; // 30 seconds
  }

  async discoverService(serviceName) {
    // Check cache first
    if (this.serviceCache.has(serviceName)) {
      const cached = this.serviceCache.get(serviceName);
      if (Date.now() - cached.timestamp < this.refreshInterval) {
        return cached.address;
      }
    }

    try {
      const services = await consul.health.service({ service: serviceName });
      const healthyServices = services.filter(service => service.Checks.every(check => check.Status === 'passing'));

      if (healthyServices.length === 0) {
        throw new Error(`No healthy instances of ${serviceName} found`);
      }

      // Round-robin selection
      const selectedService = healthyServices[Math.floor(Math.random() * healthyServices.length)];
      const address = `http://${selectedService.Service.Address}:${selectedService.Service.Port}`;

      // Cache the result
      this.serviceCache.set(serviceName, {
        address,
        timestamp: Date.now()
      });

      return address;
    } catch (error) {
      console.error(`Service discovery failed for ${serviceName}:`, error);
      throw error;
    }
  }

  async registerService(serviceName, address, port) {
    await consul.agent.service.register({
      name: serviceName,
      address: address,
      port: port,
      check: {
        http: `http://${address}:${port}/health`,
        interval: '10s',
        timeout: '1s'
      }
    });
  }
}

module.exports = new ServiceDiscovery();
```

### Service Registration
```javascript
// Auto-registration on startup
const serviceDiscovery = require('./serviceDiscovery');

const serviceName = 'user-service';
const serviceAddress = process.env.HOST || 'localhost';
const servicePort = process.env.PORT || 3000;

// Register service on startup
serviceDiscovery.registerService(serviceName, serviceAddress, servicePort)
  .then(() => {
    console.log(`${serviceName} registered successfully`);
  })
  .catch(err => {
    console.error(`Failed to register ${serviceName}:`, err);
    process.exit(1);
  });

// Deregister on shutdown
process.on('SIGTERM', async () => {
  try {
    await serviceDiscovery.deregisterService(serviceName);
    console.log(`${serviceName} deregistered`);
    process.exit(0);
  } catch (err) {
    console.error('Error during shutdown:', err);
    process.exit(1);
  }
});
```

## Inter-Service Communication

### Synchronous Communication
```javascript
// Service-to-service communication with circuit breaker
const axios = require('axios');
const CircuitBreaker = require('opossum');

class ServiceClient {
  constructor(baseURL, options = {}) {
    this.client = axios.create({
      baseURL,
      timeout: options.timeout || 5000,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'microservice-client/1.0'
      }
    });

    // Circuit breaker configuration
    this.circuitBreaker = new CircuitBreaker(
      this.makeRequest.bind(this),
      {
        timeout: 3000,        // If our function takes longer than 3 seconds, trigger a failure
        errorThresholdPercentage: 50, // When 50% of requests fail, open the circuit
        resetTimeout: 30000   // After 30 seconds, try again.
      }
    );

    this.circuitBreaker.on('open', () => {
      console.log('Circuit breaker opened for', baseURL);
    });

    this.circuitBreaker.on('close', () => {
      console.log('Circuit breaker closed for', baseURL);
    });
  }

  async makeRequest(config) {
    try {
      const response = await this.client(config);
      return response.data;
    } catch (error) {
      console.error('Service request failed:', error.message);
      throw error;
    }
  }

  async get(path, options = {}) {
    return await this.circuitBreaker.fire({
      method: 'GET',
      url: path,
      ...options
    });
  }

  async post(path, data, options = {}) {
    return await this.circuitBreaker.fire({
      method: 'POST',
      url: path,
      data,
      ...options
    });
  }
}

// Usage
const userServiceClient = new ServiceClient('http://user-service:3000');
```

### Asynchronous Communication with Message Queues
```javascript
// Event-driven communication with RabbitMQ
const amqp = require('amqplib');

class EventPublisher {
  constructor() {
    this.connection = null;
    this.channel = null;
  }

  async connect() {
    this.connection = await amqp.connect(process.env.RABBITMQ_URL);
    this.channel = await this.connection.createChannel();

    // Ensure exchange exists
    await this.channel.assertExchange('microservice_events', 'topic', { durable: true });
  }

  async publish(eventType, data) {
    if (!this.channel) {
      throw new Error('Not connected to message broker');
    }

    const message = JSON.stringify({
      type: eventType,
      data,
      timestamp: new Date().toISOString()
    });

    this.channel.publish('microservice_events', eventType, Buffer.from(message));
  }

  async disconnect() {
    if (this.channel) {
      await this.channel.close();
    }
    if (this.connection) {
      await this.connection.close();
    }
  }
}

class EventSubscriber {
  constructor(serviceName) {
    this.serviceName = serviceName;
    this.connection = null;
    this.channel = null;
  }

  async connect() {
    this.connection = await amqp.connect(process.env.RABBITMQ_URL);
    this.channel = await this.connection.createChannel();

    // Create queue for this service
    const queue = `${this.serviceName}_queue`;
    await this.channel.assertQueue(queue, { durable: true });

    // Bind to relevant events
    await this.channel.bindQueue(queue, 'microservice_events', 'user.*');
    await this.channel.bindQueue(queue, 'microservice_events', 'order.*');
  }

  async subscribe(eventHandler) {
    await this.channel.consume(this.serviceName + '_queue', async (msg) => {
      if (msg !== null) {
        try {
          const event = JSON.parse(msg.content.toString());
          await eventHandler(event);
          this.channel.ack(msg); // Acknowledge successful processing
        } catch (error) {
          console.error('Event processing failed:', error);
          this.channel.nack(msg, false, true); // Requeue the message
        }
      }
    });
  }
}
```

## Data Management in Microservices

### Database per Service Pattern
```javascript
// Each service has its own database
class UserService {
  constructor() {
    this.db = require('./database/userDb'); // Service-specific database
  }

  async getUser(userId) {
    return await this.db.users.findById(userId);
  }

  async updateUser(userId, updateData) {
    return await this.db.users.updateById(userId, updateData);
  }
}

class OrderService {
  constructor() {
    this.db = require('./database/orderDb'); // Different database
  }

  async createOrder(orderData) {
    // Validate user exists by calling user service
    try {
      await this.validateUser(orderData.userId);
    } catch (error) {
      throw new Error('User validation failed');
    }

    return await this.db.orders.create(orderData);
  }

  async validateUser(userId) {
    // Call user service to validate user exists
    const user = await userServiceClient.get(`/users/${userId}`);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }
}
```

### Saga Pattern for Distributed Transactions
```javascript
// Saga pattern for distributed transaction management
class OrderSaga {
  constructor() {
    this.steps = [];
    this.currentStep = 0;
  }

  async execute(orderData) {
    this.steps = [
      { name: 'createOrder', action: () => this.createOrder(orderData) },
      { name: 'reserveInventory', action: () => this.reserveInventory(orderData) },
      { name: 'processPayment', action: () => this.processPayment(orderData) },
      { name: 'notifyCustomer', action: () => this.notifyCustomer(orderData) }
    ];

    try {
      for (const step of this.steps) {
        await step.action();
        this.currentStep++;
      }
    } catch (error) {
      // Execute compensation steps
      await this.compensate(error);
      throw error;
    }
  }

  async compensate(error) {
    // Execute compensation steps in reverse order
    for (let i = this.currentStep - 1; i >= 0; i--) {
      const step = this.steps[i];
      try {
        await this.compensateStep(step.name, error);
      } catch (compensationError) {
        console.error(`Compensation failed for step ${step.name}:`, compensationError);
      }
    }
  }

  async compensateStep(stepName, originalError) {
    switch (stepName) {
      case 'notifyCustomer':
        // No compensation needed
        break;
      case 'processPayment':
        await this.refundPayment();
        break;
      case 'reserveInventory':
        await this.releaseInventory();
        break;
      case 'createOrder':
        await this.cancelOrder();
        break;
    }
  }

  async createOrder(orderData) {
    // Create order in order service
    return await orderService.create(orderData);
  }

  async reserveInventory(orderData) {
    // Reserve inventory in inventory service
    return await inventoryService.reserve(orderData.items);
  }

  async processPayment(orderData) {
    // Process payment in payment service
    return await paymentService.process(orderData.payment);
  }

  async notifyCustomer(orderData) {
    // Notify customer in notification service
    return await notificationService.send(orderData.customerId, 'order_created');
  }

  async refundPayment() {
    // Refund the payment
  }

  async releaseInventory() {
    // Release reserved inventory
  }

  async cancelOrder() {
    // Cancel the order
  }
}
```

## Circuit Breaker and Retry Patterns

### Circuit Breaker Implementation
```javascript
// Advanced circuit breaker with state management
class CircuitBreaker {
  constructor(options = {}) {
    this.options = {
      timeout: options.timeout || 60000,
      errorThreshold: options.errorThreshold || 5,
      resetTimeout: options.resetTimeout || 60000,
      ...options
    };

    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.failureCount = 0;
    this.lastFailureTime = null;
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.options.resetTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.options.errorThreshold) {
      this.state = 'OPEN';
    }
  }

  async withCircuitBreaker(fn) {
    return await this.call(fn);
  }
}

// Usage
const userCircuitBreaker = new CircuitBreaker({
  errorThreshold: 3,
  resetTimeout: 30000
});

const getUserWithCircuitBreaker = async (userId) => {
  return await userCircuitBreaker.withCircuitBreaker(async () => {
    return await userServiceClient.get(`/users/${userId}`);
  });
};
```

### Retry Pattern with Exponential Backoff
```javascript
// Retry mechanism with exponential backoff
const retryWithBackoff = async (fn, options = {}) => {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 10000,
    backoffMultiplier = 2,
    retryCondition = (error) => true
  } = options;

  let retryCount = 0;

  while (true) {
    try {
      return await fn();
    } catch (error) {
      retryCount++;

      if (retryCount > maxRetries || !retryCondition(error)) {
        throw error;
      }

      // Calculate delay with jitter
      const baseDelayWithMultiplier = baseDelay * Math.pow(backoffMultiplier, retryCount - 1);
      const delay = Math.min(baseDelayWithMultiplier, maxDelay);
      const jitter = Math.random() * 0.1 * delay; // 10% jitter
      const totalDelay = delay + jitter;

      console.log(`Retry attempt ${retryCount}/${maxRetries} after ${totalDelay}ms`);

      await new Promise(resolve => setTimeout(resolve, totalDelay));
    }
  }
};

// Usage
const callUserService = async (userId) => {
  return await retryWithBackoff(
    async () => {
      return await userServiceClient.get(`/users/${userId}`);
    },
    {
      maxRetries: 3,
      retryCondition: (error) => {
        // Only retry on network errors or 5xx status codes
        return error.code === 'ECONNREFUSED' ||
               error.response?.status >= 500;
      }
    }
  );
};
```

## Configuration Management

### Externalized Configuration
```javascript
// Configuration management with environment and service discovery
class ConfigManager {
  constructor() {
    this.config = {};
    this.serviceEndpoints = new Map();
  }

  async loadConfiguration() {
    // Load from environment variables
    this.config = {
      port: process.env.PORT || 3000,
      database: {
        url: process.env.DATABASE_URL,
        poolSize: process.env.DB_POOL_SIZE || 10
      },
      services: {
        userService: process.env.USER_SERVICE_URL || 'http://user-service:3000',
        orderService: process.env.ORDER_SERVICE_URL || 'http://order-service:3000'
      },
      security: {
        jwtSecret: process.env.JWT_SECRET,
        apiKey: process.env.API_KEY
      }
    };

    // Override with service discovery if available
    await this.loadServiceEndpoints();
  }

  async loadServiceEndpoints() {
    // Load service endpoints from discovery service
    try {
      const discovery = require('./serviceDiscovery');

      for (const [serviceName, defaultUrl] of Object.entries(this.config.services)) {
        try {
          const serviceUrl = await discovery.discoverService(serviceName);
          this.config.services[serviceName] = serviceUrl;
        } catch (error) {
          console.warn(`Service discovery failed for ${serviceName}, using default: ${defaultUrl}`);
          // Keep default URL
        }
      }
    } catch (error) {
      console.error('Service discovery unavailable:', error);
    }
  }

  get(key) {
    return this.config[key];
  }

  async reload() {
    await this.loadConfiguration();
  }
}

const config = new ConfigManager();
module.exports = config;
```

## Health Monitoring and Observability

### Health Check Implementation
```javascript
// Comprehensive health check for microservices
class HealthChecker {
  constructor() {
    this.checks = [];
    this.status = 'healthy';
  }

  addCheck(name, checkFunction, interval = 30000) {
    this.checks.push({
      name,
      checkFunction,
      interval,
      lastCheck: null,
      status: 'unknown',
      error: null
    });

    // Start periodic checking
    setInterval(async () => {
      await this.runCheck(name);
    }, interval);
  }

  async runCheck(name) {
    const check = this.checks.find(c => c.name === name);
    if (!check) return;

    try {
      const result = await check.checkFunction();
      check.status = result.healthy ? 'healthy' : 'unhealthy';
      check.error = result.error || null;
      check.lastCheck = new Date().toISOString();
    } catch (error) {
      check.status = 'unhealthy';
      check.error = error.message;
      check.lastCheck = new Date().toISOString();
    }

    // Update overall status
    this.updateOverallStatus();
  }

  updateOverallStatus() {
    const unhealthyChecks = this.checks.filter(c => c.status === 'unhealthy');
    this.status = unhealthyChecks.length > 0 ? 'unhealthy' : 'healthy';
  }

  getHealthStatus() {
    return {
      status: this.status,
      timestamp: new Date().toISOString(),
      checks: this.checks.map(check => ({
        name: check.name,
        status: check.status,
        lastCheck: check.lastCheck,
        error: check.error
      }))
    };
  }
}

// Usage in service
const healthChecker = new HealthChecker();

// Add various health checks
healthChecker.addCheck('database', async () => {
  try {
    await db.ping(); // Your database connection check
    return { healthy: true };
  } catch (error) {
    return { healthy: false, error: error.message };
  }
});

healthChecker.addCheck('external-api', async () => {
  try {
    await axios.get('http://external-service/health');
    return { healthy: true };
  } catch (error) {
    return { healthy: false, error: error.message };
  }
});

// Health endpoint
app.get('/health', (req, res) => {
  const status = healthChecker.getHealthStatus();
  const statusCode = status.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(status);
});
```

## Deployment Patterns

### Blue-Green Deployment
```javascript
// Configuration for blue-green deployment
const deploymentConfig = {
  blue: {
    version: process.env.BLUE_VERSION || 'v1',
    url: process.env.BLUE_SERVICE_URL || 'http://service-blue:3000',
    weight: 0 // Start with 0% traffic
  },
  green: {
    version: process.env.GREEN_VERSION || 'v1',
    url: process.env.GREEN_SERVICE_URL || 'http://service-green:3000',
    weight: 100 // Start with 100% traffic
  },
  current: 'green' // Current active deployment
};

// Traffic routing middleware
const routeTraffic = (req, res, next) => {
  const target = determineTargetDeployment();
  req.targetService = deploymentConfig[target].url;
  next();
};

const determineTargetDeployment = () => {
  // For blue-green, we can hardcode or use a feature flag
  return deploymentConfig.current;
};

// Health check for new deployment before switching traffic
const validateDeployment = async (deployment) => {
  const url = deploymentConfig[deployment].url;

  try {
    const response = await axios.get(`${url}/health`);
    if (response.data.status === 'healthy') {
      // Switch traffic to new deployment
      deploymentConfig.current = deployment;
      console.log(`Traffic switched to ${deployment} deployment`);
      return true;
    }
  } catch (error) {
    console.error(`Health check failed for ${deployment} deployment:`, error);
  }

  return false;
};
```

This guide provides comprehensive microservices architecture patterns for production applications, covering service decomposition, communication, data management, and operational concerns.