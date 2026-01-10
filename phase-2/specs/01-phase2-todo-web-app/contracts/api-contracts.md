# API Contracts: Phase-2 Todo Web Application

**Date**: 2026-01-03
**Feature**: Phase-2 Todo Web Application
**Branch**: 01-phase2-todo-web-app

## Overview

This document defines the API contracts for the Phase-2 Todo Web Application. All endpoints require JWT token authentication in the Authorization header unless explicitly noted as public.

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## API Endpoints

### Task Management

#### Create Task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-200 chars)",
    "description": "string (optional, max 1000 chars)"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Error Responses**:
  - `400 Bad Request` - Invalid input
  - `401 Unauthorized` - Invalid JWT token
  - `403 Forbidden` - User ID mismatch
  - `500 Internal Server Error` - Server error

#### Get All Tasks
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Auth Required**: Yes
- **Query Parameters**:
  - `status`: "all" | "pending" | "completed" (default: "all")
  - `sort`: "created" | "title" | "due_date" (default: "created")
- **Success Response**: `200 OK`
  ```json
  {
    "tasks": [
      {
        "id": "integer",
        "user_id": "string",
        "title": "string",
        "description": "string",
        "completed": "boolean",
        "created_at": "datetime",
        "updated_at": "datetime"
      }
    ],
    "total_count": "integer",
    "completed_count": "integer",
    "pending_count": "integer"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized` - Invalid JWT token
  - `403 Forbidden` - User ID mismatch
  - `500 Internal Server Error` - Server error

#### Get Specific Task
- **Endpoint**: `GET /api/{user_id}/tasks/{id}`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized` - Invalid JWT token
  - `403 Forbidden` - User ID mismatch
  - `404 Not Found` - Task not found
  - `500 Internal Server Error` - Server error

#### Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{id}`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "string (optional, 1-200 chars)",
    "description": "string (optional, max 1000 chars)"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Error Responses**:
  - `400 Bad Request` - Invalid input
  - `401 Unauthorized` - Invalid JWT token
  - `403 Forbidden` - User ID mismatch
  - `404 Not Found` - Task not found
  - `500 Internal Server Error` - Server error

#### Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{id}`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized` - Invalid JWT token
  - `403 Forbidden` - User ID mismatch
  - `404 Not Found` - Task not found
  - `500 Internal Server Error` - Server error

#### Toggle Task Completion
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "completed": "boolean (optional, default: toggle current status)"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized` - Invalid JWT token
  - `403 Forbidden` - User ID mismatch
  - `404 Not Found` - Task not found
  - `500 Internal Server Error` - Server error

## Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "code": "error_code_string",
    "message": "human_readable_error_message",
    "details": "optional_error_details"
  }
}
```

## Common HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required/failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error