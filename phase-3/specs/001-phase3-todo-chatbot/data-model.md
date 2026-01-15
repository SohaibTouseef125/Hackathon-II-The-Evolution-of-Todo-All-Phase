# Data Model: Todo AI Chatbot

## Entity Relationships

```
User (Better Auth) 1 ←→ * Task
User (Better Auth) 1 ←→ * Conversation
User (Better Auth) 1 ←→ * Message
Conversation 1 ←→ * Message
```

## Entity Definitions

### Task
**Purpose**: Represents a user's todo item with status and metadata

**Attributes**:
- `user_id`: string (required, foreign key to Better Auth user)
- `id`: integer (primary key, auto-incremented)
- `title`: string (required, 1-200 characters)
- `description`: string (optional, max 1000 characters)
- `completed`: boolean (default false)
- `created_at`: timestamp (auto-generated)
- `updated_at`: timestamp (auto-generated, updated on modification)

**Validation Rules**:
- Title must be 1-200 characters
- Description must be max 1000 characters if provided
- User_id must match authenticated user
- Cannot modify tasks belonging to other users

**State Transitions**:
- `pending` → `completed` when complete_task is called
- `completed` → `pending` when complete_task is called again

### Conversation
**Purpose**: Groups related messages in a chat session

**Attributes**:
- `user_id`: string (required, foreign key to Better Auth user)
- `id`: integer (primary key, auto-incremented)
- `created_at`: timestamp (auto-generated)
- `updated_at`: timestamp (auto-generated, updated when new messages added)

**Validation Rules**:
- User_id must match authenticated user
- Cannot access conversations belonging to other users

### Message
**Purpose**: Stores individual communications in a conversation with emphasis on conversation history preservation

**Attributes**:
- `user_id`: string (required, foreign key to Better Auth user)
- `id`: integer (primary key, auto-incremented)
- `conversation_id`: integer (required, foreign key to Conversation)
- `role`: string (required, "user" or "assistant")
- `content`: string (required, message content)
- `created_at`: timestamp (auto-generated)

**Validation Rules**:
- User_id must match authenticated user
- conversation_id must exist and belong to user
- Role must be either "user" or "assistant"
- Cannot access messages belonging to other users

**Conversation History Preservation**:
- All messages must be permanently stored to maintain conversation context
- Message ordering preserved by created_at timestamp
- Conversation history must be fully reconstructible for ChatKit widget functionality

### User (Better Auth - External)
**Purpose**: Authenticated user identity for task ownership and access control

**Attributes** (managed by Better Auth):
- `id`: string (primary key)
- `email`: string (unique)
- `name`: string (optional)

**Note**: User data is managed by Better Auth and referenced via user_id in our application tables.

## Database Constraints

### Primary Keys
- Each entity has an auto-incremented integer primary key
- Ensures unique identification of each record

### Foreign Keys
- Task.user_id references Better Auth user.id
- Message.conversation_id references Conversation.id
- Message.user_id references Better Auth user.id
- Conversation.user_id references Better Auth user.id

### Indexes
- Index on Task.user_id for efficient user-based queries
- Index on Task.completed for status filtering
- Index on Conversation.user_id for efficient user-based queries
- Index on Message.user_id for efficient user-based queries
- Index on Message.conversation_id for conversation-based queries

## Security Considerations

### Data Isolation
- All queries must be filtered by user_id
- MCP tools must validate that user_id matches authenticated user
- No cross-user data access is permitted

### Access Control
- Users can only read/write their own tasks
- Users can only read/write their own conversations
- Users can only read/write their own messages
- Backend must enforce user_id matching for all operations

## API Considerations

### Filtering
- All endpoints should support user_id filtering
- List operations should only return user's own data
- Individual record access should validate ownership

### Pagination
- Task listing endpoints should support pagination for large datasets
- Conversation history endpoints should support pagination
- Message history endpoints should support pagination

### Performance
- Indexes should be created on frequently queried fields
- Query optimization needed for conversation history retrieval
- Consider caching for frequently accessed data