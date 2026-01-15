---
name: phase3-todo-chatbot
description: Complete Phase 3 implementation combining OpenAI ChatKit, Agents SDK, and MCP Server for AI-powered todo management via natural language. Use when building the full todo chatbot with conversational interface and task operations.
---

# Phase 3 Todo Chatbot

Complete implementation combining OpenAI ChatKit, Agents SDK, and MCP Server for AI-powered todo management.

## Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐
│                 │     │              FastAPI Server                   │
│  ChatKit UI     │────▶│  ┌────────────────────────────────────────┐  │
│  (Frontend)     │     │  │         Chat Endpoint                  │  │
│                 │     │  │  POST /api/{user_id}/chat             │  │
│                 │     │  └───────────────┬────────────────────────┘  │
│                 │     │                  │                           │
│                 │     │                  ▼                           │
│                 │     │  ┌────────────────────────────────────────┐  │
│                 │◀────│  │      OpenAI Agents SDK                 │  │
│                 │     │  │      (Agent + Runner)                  │  │
│                 │     │  └───────────────┬────────────────────────┘  │
│                 │     │                  │                           │
│                 │     │                  ▼                           │
│                 │     │  ┌────────────────────────────────────────┐  │
│                 │     │  │         MCP Server                     │  │
│                 │     │  │  (MCP Tools for Task Operations)       │  │
│                 │     │  └────────────────────────────────────────┘  │
│                 │     └──────────────────────────────────────────────┘
│                 │                           │
│                 ▼                           ▼
│          ┌──────────────────────────────────────────┐
│          │            Neon DB (PostgreSQL)          │
│          │  - tasks  |  - conversations  | - messages│
│          └──────────────────────────────────────────┘
```

## Implementation Steps

### 1. Database Models

```python
# models.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    messages: list["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    user_id: str = Field(index=True)
    role: str  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    conversation: Conversation | None = Relationship(back_populates="messages")
```

### 2. MCP Server with Task Tools

```python
# mcp_server.py
from mcp.server import Server
from mcp.types import Tool, TextContent
from models import Task

app = Server("todo-mcp-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_task",
            description="Create a new task for the user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List tasks with optional status filter",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update task title or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    from db import get_session

    with get_session() as session:
        if name == "add_task":
            task = Task(
                user_id=arguments["user_id"],
                title=arguments["title"],
                description=arguments.get("description")
            )
            session.add(task)
            session.commit()
            return [TextContent(type="text", text=f"Created task {task.id}: {task.title}")]

        elif name == "list_tasks":
            query = session.query(Task).filter(Task.user_id == arguments["user_id"])
            if arguments.get("status") == "pending":
                query = query.filter(Task.completed == False)
            elif arguments.get("status") == "completed":
                query = query.filter(Task.completed == True)
            tasks = query.all()
            return [TextContent(type="text", text=str([{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]))]

        elif name == "complete_task":
            task = session.query(Task).filter(
                Task.id == arguments["task_id"],
                Task.user_id == arguments["user_id"]
            ).first()
            if task:
                task.completed = True
                session.commit()
                return [TextContent(type="text", text=f"Completed task {task.id}: {task.title}")]
            return [TextContent(type="text", text="Task not found")]

        # Similar handlers for delete_task, update_task...
```

### 3. Chat API Endpoint

```python
# main.py
from fastapi import FastAPI
from agents import Agent, Runner
from models import Conversation, Message

app = FastAPI()

# Define todo agent with MCP tools
todo_agent = Agent(
    name="Todo Assistant",
    instructions="""You are a helpful todo assistant. Help users manage their tasks through natural language.

    When users want to:
    - Add/create/remember something → use add_task
    - See/list/show tasks → use list_tasks
    - Mark complete/done/finished → use complete_task
    - Delete/remove/cancel → use delete_task
    - Change/update/rename → use update_task

    Always confirm actions with friendly responses.""",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)

class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str

@app.post("/api/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest):
    from db import get_session

    with get_session() as session:
        # Get or create conversation
        if request.conversation_id:
            conversation = session.query(Conversation).filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user_id
            ).first()
        else:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()

        # Fetch history
        messages = session.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at).all()

        # Build message array
        message_history = [{"role": m.role, "content": m.content} for m in messages]

        # Store user message
        user_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message
        )
        session.add(user_msg)
        session.commit()

        # Run agent
        agent_input = message_history + [{"role": "user", "content": request.message}]
        result = Runner.run(todo_agent, input=agent_input)

        # Store assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=result.final_output
        )
        session.add(assistant_msg)
        session.commit()

        return {
            "conversation_id": conversation.id,
            "response": result.final_output,
            "tool_calls": []
        }
```

### 4. Frontend with ChatKit

```tsx
// app/chat/[userId]/page.tsx
'use client'

import ChatKit from '@openai/chatkit'

export default function ChatPage({ params }: { params: { userId: string } }) {
  return (
    <div className="h-screen">
      <ChatKit
        apiUrl={`http://localhost:8000/api/${params.userId}/chat`}
        domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || ''}
        title="Todo Assistant"
        welcomeMessage="Hi! I can help you manage your tasks. Try saying 'Add a task to buy groceries' or 'What tasks do I have?'"
      />
    </div>
  )
}
```

## Natural Language Commands

| User Says | Agent Action |
|-----------|--------------|
| "Add a task to buy groceries" | Call `add_task` with title "Buy groceries" |
| "Show me all my tasks" | Call `list_tasks` with status "all" |
| "What's pending?" | Call `list_tasks` with status "pending" |
| "Mark task 3 as complete" | Call `complete_task` with task_id 3 |
| "Delete the meeting task" | Call `list_tasks` first, then `delete_task` |
| "Change task 1 to 'Call mom tonight'" | Call `update_task` with new title |
| "What have I completed?" | Call `list_tasks` with status "completed" |

## Environment Variables

```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host/db
OPENAI_API_KEY=sk-...

# Frontend (.env.local)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
```

## See Also

- [OpenAI ChatKit Skill](../openai-chatkit/SKILL.md) - Frontend UI
- [OpenAI Agents SDK Skill](../openai-agents-sdk/SKILL.md) - Agent logic
- [MCP Server Python Skill](../mcp-server-python/SKILL.md) - Tool definitions
- [Stateless Chatbot Architecture](../stateless-chatbot-architecture/SKILL.md) - Request cycle
