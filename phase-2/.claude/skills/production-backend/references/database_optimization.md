# Database Design and Query Optimization Techniques

## Database Design Principles

### Normalization
- **First Normal Form (1NF)**: Eliminate repeating groups, ensure atomic values
- **Second Normal Form (2NF)**: Remove partial dependencies
- **Third Normal Form (3NF)**: Remove transitive dependencies
- **Benefits**: Reduce data redundancy, improve data integrity

### Denormalization Strategies
- When to denormalize for performance
- Balancing consistency vs. performance
- Read replicas for read-heavy applications

## Indexing Strategies

### Index Types
- **B-Tree Indexes**: Default for most databases, good for range queries
- **Hash Indexes**: Fast for exact matches, no range queries
- **Full-Text Indexes**: For text search operations
- **Composite Indexes**: Multiple columns, order matters

### Index Best Practices
```sql
-- Good: Create index for frequently queried columns
CREATE INDEX idx_users_email ON users(email);

-- Good: Composite index with proper column order
CREATE INDEX idx_users_status_created ON users(status, created_at);

-- Good: Partial index for filtered queries
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Bad: Indexing every column
-- Avoid: Too many indexes slow down writes
```

### When to Index
- Columns in WHERE clauses
- Columns in JOIN conditions
- Columns in ORDER BY clauses
- Foreign key columns

## Query Optimization

### Writing Efficient Queries

#### SELECT Clause
```sql
-- Good: Select only needed columns
SELECT id, name, email FROM users WHERE active = true;

-- Bad: Select all columns when not needed
SELECT * FROM users WHERE active = true;
```

#### JOIN Optimization
```sql
-- Good: Use appropriate JOIN types
SELECT u.name, p.title
FROM users u
INNER JOIN posts p ON u.id = p.user_id
WHERE u.active = true;

-- Good: Join order matters - start with most selective table
SELECT u.name, p.title
FROM users u  -- Assume this is filtered first
INNER JOIN posts p ON u.id = p.user_id  -- Then join to posts
WHERE u.status = 'active' AND p.published = true;
```

#### Subquery Optimization
```sql
-- Prefer JOIN over correlated subqueries
-- Good:
SELECT u.name, u.email
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created_at > '2023-01-01';

-- Avoid correlated subqueries when possible:
SELECT u.name, u.email
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id
    AND o.created_at > '2023-01-01'
);
```

### Query Execution Plan Analysis

#### PostgreSQL Example
```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';
```

#### Key Metrics to Watch
- **Cost**: Estimated cost of the operation
- **Rows**: Estimated number of rows processed
- **Time**: Actual execution time
- **Index usage**: Whether indexes are being used effectively

## NoSQL Database Patterns

### MongoDB Optimization

#### Schema Design
```javascript
// Good: Embed related data that's frequently accessed together
{
  _id: ObjectId("..."),
  name: "John Doe",
  email: "john@example.com",
  orders: [
    {
      order_id: "order123",
      date: ISODate("2023-01-01"),
      items: [...]
    }
  ]
}

// Good: Reference when data is large or frequently updated separately
{
  _id: ObjectId("..."),
  name: "John Doe",
  email: "john@example.com",
  order_ids: ["order123", "order456"]
}
```

#### Indexing in MongoDB
```javascript
// Single field index
db.users.createIndex({ email: 1 })

// Compound index
db.users.createIndex({ status: 1, created_at: -1 })

// Text index
db.posts.createIndex({ title: "text", content: "text" })

// TTL index for automatic cleanup
db.sessions.createIndex({ "createdAt": 1 }, { expireAfterSeconds: 3600 })
```

### Redis Optimization

#### Data Structure Selection
```javascript
// Use appropriate data structures
// Strings for simple key-value
SET user:123 "John Doe"

// Hashes for objects
HSET user:123 name "John Doe" email "john@example.com" age 30

// Lists for queues
LPUSH job_queue "job_data"

// Sets for unique collections
SADD user_interests:123 "technology" "sports" "music"

// Sorted sets for ranked data
ZADD leaderboard user_id score
```

## Connection Pooling

### Pool Configuration
```javascript
// Example with database connection pool
const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'myapp',
  user: 'myuser',
  password: 'mypass',
  // Pool configuration
  min: 2,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### Pool Best Practices
- Set appropriate min/max connections
- Configure connection timeouts
- Handle connection failures gracefully
- Monitor pool usage

## Caching Strategies

### Database Query Caching
```javascript
// Example caching pattern
const getUserWithCache = async (id) => {
  // Try cache first
  const cached = await redis.get(`user:${id}`);
  if (cached) {
    return JSON.parse(cached);
  }

  // Query database
  const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);

  // Cache result
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));

  return user;
};
```

### Cache Invalidation
- Time-based expiration (TTL)
- Event-based invalidation
- Write-through vs write-behind caching

## Performance Monitoring

### Key Metrics
- Query execution time
- Database connection usage
- Cache hit/miss ratios
- Index usage statistics
- Slow query logs

### Query Analysis Tools
```sql
-- PostgreSQL: Find slow queries
SELECT query, mean_time, calls
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- MySQL: Slow query log analysis
SET long_query_time = 1;  -- Log queries taking more than 1 second
```

## Migration Strategies

### Zero-Downtime Migrations
1. Backward compatible changes first
2. Deploy application code that works with both schemas
3. Run database migration
4. Deploy code that removes old behavior

### Large Data Migrations
```javascript
// Batch processing for large datasets
const migrateInBatches = async (batchSize = 1000) => {
  let offset = 0;
  let processed = 0;

  do {
    const records = await db.query(
      `SELECT * FROM old_table LIMIT $1 OFFSET $2`,
      [batchSize, offset]
    );

    if (records.length === 0) break;

    // Process batch
    for (const record of records) {
      await processRecord(record);
    }

    processed += records.length;
    offset += batchSize;

    // Add delay to avoid overwhelming the database
    await new Promise(resolve => setTimeout(resolve, 100));
  } while (true);
};
```

## Common Database Performance Issues

### N+1 Query Problem
```javascript
// Bad: N+1 queries
const users = await User.findAll();
for (const user of users) {
  // This executes one query per user
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// Good: Single query with join
const usersWithPosts = await User.findAll({
  include: [{ model: Post }]
});
```

### Cartesian Explosion
```sql
-- Problem: Joining multiple one-to-many relationships
SELECT u.name, p.title, c.content
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
LEFT JOIN comments c ON p.id = c.post_id;

-- Solution: Separate queries or use subqueries
```

This guide provides comprehensive database optimization techniques for production applications, covering both SQL and NoSQL databases with practical examples and best practices.