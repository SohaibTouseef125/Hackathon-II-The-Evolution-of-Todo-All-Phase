# Todo AI Chatbot API Specification

## Overview
This document describes the API endpoints for the Todo AI Chatbot application.

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Chat Endpoint
Handles natural language interactions with the AI assistant for task management.

- **URL**: `/api/{user_id}/chat`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Path Parameters**:
  - `user_id`: The UUID of the authenticated user
- **Headers**:
  - `Authorization`: Bearer token
  - `Content-Type`: application/json
- **Request Body**:
  ```json
  {
    "message": "string (required, max 500 chars)",
    "conversation_id": "string (optional, UUID format)"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "conversation_id": "string (UUID)",
      "response": "string",
      "tool_calls": "array"
    }
    ```
- **Error Responses**:
  - **Code**: 401 - Unauthorized (Invalid or missing token)
  - **Code**: 403 - Forbidden (User trying to access another user's data)
  - **Code**: 422 - Unprocessable Entity (Invalid input data)
  - **Code**: 500 - Internal Server Error

## Validation Rules

### Task Creation
- Title is required and must be 1-200 characters
- Description must be 1000 characters or less if provided
- User must be authenticated

### Task Updates
- Task ID must be a valid UUID
- Title must be 1-200 characters if provided
- Description must be 1000 characters or less if provided
- User must own the task being updated

### Message Input
- Message must be provided and non-empty
- Message must be a string
- Message length limited to 500 characters

### Conversation ID
- If provided, must be a valid UUID format
- User must have access to the conversation

## Error Handling
The API returns appropriate HTTP status codes and descriptive error messages:
- 401: Authentication required or token invalid
- 403: User attempting to access unauthorized resources
- 422: Validation errors or malformed requests
- 500: Server-side errors

## Security Measures
- JWT-based authentication required for all endpoints
- User isolation enforced - users can only access their own data
- Input sanitization to prevent prompt injection
- Rate limiting should be implemented in production