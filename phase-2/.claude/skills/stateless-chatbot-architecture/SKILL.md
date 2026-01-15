---
name: stateless-chatbot-architecture
description: Stateless chatbot architecture pattern for scalable conversational AI. Use when building chat endpoints that maintain conversation state in a database rather than server memory, enabling horizontal scaling and resilience.
---

# Stateless Chatbot Architecture

Build scalable chatbots where the server holds no state between requests. All conversation context is persisted to the database.

## Request Cycle

```
1. Receive user message + conversation_id (or none)
2. Fetch conversation history from database
3. Build message array: [history messages] + [new user message]
4. Store user message in database
5. Run agent with MCP tools
6. Store assistant response in database
7. Return response to client
8. Server holds NO state (ready for next request)
```

## Database Schema

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Chat API Endpoint

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents import Runner
from models import Conversation, Message

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list

@router.post("/api/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest):
    # Step 1: Get or create conversation
    if request.conversation_id:
        conversation = db.session.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == user_id
        ).first()
    else:
        conversation = Conversation(user_id=user_id)
        db.session.add(conversation)
        db.session.commit()

    # Step 2: Fetch conversation history
    messages = db.session.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()

    # Step 3: Build message array for agent
    message_history = [
        {"role": m.role, "content": m.content}
        for m in messages
    ]

    # Step 4: Store user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message
    )
    db.session.add(user_message)
    db.session.commit()

    # Step 5: Run agent with full context
    agent_input = message_history + [{"role": "user", "content": request.message}]

    result = Runner.run(
        todo_agent,
        input=agent_input
    )

    # Step 6: Store assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=result.final_output
    )
    db.session.add(assistant_message)

    # Update conversation timestamp
    conversation.updated_at = func.now()
    db.session.commit()

    # Step 7: Return response (no state held)
    return ChatResponse(
        conversation_id=conversation.id,
        response=result.final_output,
        tool_calls=[]
    )
```

## Benefits

| Aspect | Benefit |
|--------|---------|
| **Scalability** | Any server instance handles any request |
| **Resilience** | Server restarts don't lose conversation state |
| **Horizontal scaling** | Load balancer routes to any backend |
| **Testability** | Each request is independent and reproducible |
| **Cost efficiency** | Stateless servers can scale to zero |

## Error Handling

```python
@router.post("/api/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest):
    try:
        # ... main logic ...
    except ConversationNotFound:
        raise HTTPException(status_code=404, detail="Conversation not found")
    except AgentError as e:
        # Log error, return user-friendly message
        return ChatResponse(
            conversation_id=conversation.id,
            response="I encountered an error. Please try again.",
            tool_calls=[]
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## See Also

- [Phase 3 Todo Chatbot Skill](../phase3-todo-chatbot/SKILL.md) - Complete implementation
- [OpenAI Agents SDK Skill](../openai-agents-sdk/SKILL.md) - For agent logic
- [MCP Server Python Skill](../mcp-server-python/SKILL.md) - For tool definitions
