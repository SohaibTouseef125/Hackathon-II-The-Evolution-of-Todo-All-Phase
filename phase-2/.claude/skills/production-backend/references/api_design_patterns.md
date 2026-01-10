# RESTful API Design and Best Practices

## API Design Principles

### Resource Naming
- Use nouns to represent resources (e.g., `/users`, `/orders`)
- Use plural nouns for collections (e.g., `/users` not `/user`)
- Use HTTP methods to indicate the action (GET, POST, PUT, DELETE)
- Use sub-resources for relationships (e.g., `/users/{id}/orders`)

### HTTP Methods
- **GET**: Retrieve a resource or collection
- **POST**: Create a new resource
- **PUT**: Update an entire resource
- **PATCH**: Partially update a resource
- **DELETE**: Remove a resource

### Status Codes
- **200**: Success for GET, PUT, PATCH
- **201**: Created for POST
- **204**: No Content for DELETE
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **409**: Conflict
- **422**: Unprocessable Entity
- **500**: Internal Server Error

## API Versioning

### URL Versioning
```
/api/v1/users
/api/v2/users
```

### Header Versioning
```
Accept: application/vnd.myapi.v1+json
```

### Query Parameter Versioning
```
/api/users?version=1
```

## Query Parameters

### Filtering
```
GET /api/users?status=active&role=admin
```

### Sorting
```
GET /api/users?sort=created_at&order=desc
GET /api/users?sort=first_name,-last_name  // first_name ascending, last_name descending
```

### Pagination
```
GET /api/users?page=2&limit=10
GET /api/users?offset=20&limit=10
```

## Request and Response Format

### Request Body Format
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```

### Response Format
```json
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2023-01-01T00:00:00Z"
  }
}
```

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

## Security Best Practices

### Authentication Headers
```
Authorization: Bearer <token>
```

### Rate Limiting Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1609459200
```

## API Documentation

### OpenAPI Specification Example
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: Get all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: A list of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
```

## API Gateway Patterns

### Request Transformation
- Convert between different data formats
- Add authentication headers
- Transform request/response structures

### Response Caching
- Cache responses based on request parameters
- Implement cache invalidation strategies
- Handle cache headers properly

## Common API Anti-patterns to Avoid

1. Using HTTP verbs incorrectly
2. Returning inconsistent response formats
3. Not implementing proper error handling
4. Exposing internal database identifiers directly
5. Not implementing rate limiting
6. Missing API versioning strategy
7. Not implementing proper authentication/authorization