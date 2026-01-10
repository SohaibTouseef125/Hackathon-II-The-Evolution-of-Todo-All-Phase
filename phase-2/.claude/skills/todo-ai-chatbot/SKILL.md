---
name: todo-ai-chatbot
description: Comprehensive AI-powered todo chatbot with OpenAI Agents SDK and MCP server architecture. Use when Claude needs to work with the Phase III Hackathon II todo chatbot for creating conversational interfaces for todo management, implementing OpenAI Agents SDK with MCP tools, building stateless chat endpoints with database persistence, following spec-driven development practices, or any other Phase III todo AI chatbot tasks.
---

# Todo AI Chatbot - Phase III

## Overview

This skill provides comprehensive guidance for building an AI-powered chatbot interface for managing todos through natural language as part of Hackathon II Phase III. It includes OpenAI ChatKit frontend, FastAPI backend with OpenAI Agents SDK, MCP server for task operations, and stateless architecture with database persistence for conversation history.

## Core Capabilities

### 1. Conversational Interface (OpenAI ChatKit)
- Natural language processing for todo commands
- Chat interface with message history
- Context-aware responses
- Multi-turn conversation management
- Error handling and clarifications

### 2. AI Agent Integration (OpenAI Agents SDK)
- Agent configuration and setup
- Tool integration for task operations
- Response generation and formatting
- Function calling for task operations
- Conversation state management

### 3. MCP Server Architecture (Official MCP SDK)
- MCP tools for task operations (add, list, complete, delete, update)
- Standardized tool interfaces
- Integration with backend services
- State management for tool operations
- Secure tool access and permissions

### 4. Stateless Architecture
- Database persistence for conversation history
- No server-side session state
- Horizontal scalability
- Session restoration after server restart
- Conversation context management

## Project Structure

### Recommended Monorepo Structure
```
todo-ai-chatbot/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── chatbot-interaction.md
│   ├── api/
│   │   └── mcp-tools.md
│   ├── database/
│   │   └── schema.md
│   └── ai/
│       ├── agent-spec.md
│       └── conversation-flow.md
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── api/
│   │       └── chat/
│   │           └── route.ts
│   ├── components/
│   │   ├── chat/
│   │   └── ui/
│   ├── lib/
│   │   ├── chat.ts
│   │   └── api.ts
│   ├── package.json
│   └── next.config.js
├── backend/
│   ├── main.py
│   ├── agents/
│   │   ├── chat_agent.py
│   │   └── task_agent.py
│   ├── mcp_server/
│   │   ├── server.py
│   │   └── tools.py
│   ├── models/
│   │   ├── task.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── database.py
│   ├── schemas/
│   │   └── chat.py
│   └── requirements.txt
├── docker-compose.yml
├── CLAUDE.md
└── README.md
```

## Frontend Implementation (OpenAI ChatKit)

### 1. Chat Component Setup
```tsx
// frontend/components/chat/chat-interface.tsx
'use client';

import { useState } from 'react';
import { useChat } from 'ai/react';

export default function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((message) => (
          <div key={message.id} className={`mb-4 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
            <div className={`inline-block p-3 rounded-lg ${message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
              {message.content}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t">
        <input
          value={input}
          placeholder="Ask me to manage your todos..."
          onChange={handleInputChange}
          className="w-full p-3 border rounded-lg"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading} className="mt-2 p-3 bg-blue-500 text-white rounded-lg">
          Send
        </button>
      </form>
    </div>
  );
}
```

### 2. Chat API Route
```tsx
// frontend/app/api/chat/route.ts
import { Configuration, OpenAIApi } from 'openai';
import { Ratelimit } from '@upstash/ratelimit';
import { kv } from '@vercel/kv';
import { OpenAIStream, StreamingTextResponse } from 'ai';

const config = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(config);

export async function POST(req: Request) {
  // Rate limiting
  if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
    const ip = req.headers.get('x-forwarded-for');
    const ratelimit = new Ratelimit({
      redis: kv,
      limiter: Ratelimit.slidingWindow(10, '10s'),
    });

    const { success } = await ratelimit.limit(ip || 'anonymous');
    if (!success) {
      return new Response('Rate limited', { status: 429 });
    }
  }

  const { messages } = await req.json();

  const response = await openai.createChatCompletion({
    model: 'gpt-3.5-turbo',
    stream: true,
    messages,
  });

  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}
```

## Backend Implementation (FastAPI + Agents SDK)

### 1. Database Models
```python
# backend/models/conversation.py
from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from datetime import datetime

class MessageBase(SQLModel):
    role: str  # 'user' or 'assistant'
    content: str

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2. MCP Server for Task Operations
```python
# backend/mcp_server/tools.py
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import Tool, TextContent, Prompt
import asyncio
from backend.database import get_session
from backend.models.task import Task
from sqlmodel import select

class TaskMCPTools:
    def __init__(self):
        self._server = Server("todo-mcp-server")
        self._register_tools()

    def _register_tools(self):
        # Add task tool
        @self._server.tool(
            "add_task",
            description="Create a new task",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"}
                },
                "required": ["user_id", "title"]
            }
        )
        async def add_task(params: Dict[str, Any]) -> Dict[str, Any]:
            user_id = params["user_id"]
            title = params["title"]
            description = params.get("description", "")

            # Create task in database
            with get_session() as session:
                task = Task(
                    user_id=user_id,
                    title=title,
                    description=description,
                    completed=False
                )
                session.add(task)
                session.commit()
                session.refresh(task)

            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }

        # List tasks tool
        @self._server.tool(
            "list_tasks",
            description="List tasks for a user",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        )
        async def list_tasks(params: Dict[str, Any]) -> Dict[str, Any]:
            user_id = params["user_id"]
            status = params.get("status", "all")

            with get_session() as session:
                query = select(Task).where(Task.user_id == user_id)

                if status == "pending":
                    query = query.where(Task.completed == False)
                elif status == "completed":
                    query = query.where(Task.completed == True)

                tasks = session.exec(query).all()

            return {
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "completed": task.completed,
                        "description": task.description
                    }
                    for task in tasks
                ]
            }

        # Complete task tool
        @self._server.tool(
            "complete_task",
            description="Mark a task as complete",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "task_id": {"type": "integer", "description": "Task ID"}
                },
                "required": ["user_id", "task_id"]
            }
        )
        async def complete_task(params: Dict[str, Any]) -> Dict[str, Any]:
            user_id = params["user_id"]
            task_id = params["task_id"]

            with get_session() as session:
                task = session.get(Task, task_id)
                if task and task.user_id == user_id:
                    task.completed = True
                    session.add(task)
                    session.commit()
                    return {
                        "task_id": task.id,
                        "status": "completed",
                        "title": task.title
                    }
                else:
                    return {"error": "Task not found or unauthorized"}
```

### 3. AI Agent with MCP Tools
```python
# backend/agents/task_agent.py
from openai import OpenAI
from typing import Dict, Any, List
import json
from backend.mcp_server.tools import TaskMCPTools
from sqlmodel import select

class TaskAgent:
    def __init__(self):
        self.client = OpenAI(api_key=process.env.OPENAI_API_KEY)
        self.mcp_tools = TaskMCPTools()

    async def process_message(self, user_id: str, message: str, conversation_history: List[Dict]) -> str:
        # Define available tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "task_id": {"type": "integer"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

        # Prepare messages for the AI
        ai_messages = [
            {"role": "system", "content": "You are a helpful todo assistant. Use the provided functions to manage tasks for the user. Always confirm actions with the user before performing them."}
        ]

        # Add conversation history
        for msg in conversation_history:
            ai_messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current user message
        ai_messages.append({"role": "user", "content": message})

        # Call OpenAI with tools
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=ai_messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            # Execute tool calls
            available_functions = {
                "add_task": self.add_task,
                "list_tasks": self.list_tasks,
                "complete_task": self.complete_task,
            }

            messages = [response_message]

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                # Add user_id to function args
                function_args["user_id"] = user_id

                function_response = await function_to_call(**function_args)

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                })

            # Get final response from AI
            second_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )

            return second_response.choices[0].message.content
        else:
            # No tool calls, return the AI's response directly
            return response_message.content
```

### 4. Chat API Endpoint
```python
# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.agents.task_agent import TaskAgent
from backend.models.conversation import Conversation, Message
from backend.database import get_session
from sqlmodel import select

app = FastAPI(title="Todo AI Chatbot API")

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[List[Dict[str, Any]]] = None

@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    agent = TaskAgent()

    # Get or create conversation
    with get_session() as session:
        if request.conversation_id:
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation or conversation.user_id != request.user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation(user_id=request.user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Store user message
        user_message = Message(
            role="user",
            content=request.message,
            conversation_id=conversation.id,
            user_id=request.user_id
        )
        session.add(user_message)
        session.commit()

    # Get conversation history for context
    with get_session() as session:
        history_messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
        ).all()

        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages
        ]

    # Process with AI agent
    ai_response = await agent.process_message(
        request.user_id,
        request.message,
        conversation_history
    )

    # Store AI response
    with get_session() as session:
        ai_message = Message(
            role="assistant",
            content=ai_response,
            conversation_id=conversation.id,
            user_id=request.user_id
        )
        session.add(ai_message)
        session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=ai_response
    )
```

## MCP Tools Specification

### 1. add_task Tool
- **Purpose**: Create a new task
- **Parameters**:
  - `user_id` (string, required): User identifier
  - `title` (string, required): Task title
  - `description` (string, optional): Task description
- **Returns**: Object with `task_id`, `status`, and `title`

### 2. list_tasks Tool
- **Purpose**: Retrieve tasks from the list
- **Parameters**:
  - `user_id` (string, required): User identifier
  - `status` (string, optional): Filter by status ("all", "pending", "completed")
- **Returns**: Array of task objects with id, title, completed status, and description

### 3. complete_task Tool
- **Purpose**: Mark a task as complete
- **Parameters**:
  - `user_id` (string, required): User identifier
  - `task_id` (integer, required): Task identifier
- **Returns**: Object with `task_id`, `status`, and `title`

### 4. delete_task Tool
- **Purpose**: Remove a task from the list
- **Parameters**:
  - `user_id` (string, required): User identifier
  - `task_id` (integer, required): Task identifier
- **Returns**: Object with `task_id`, `status`, and `title`

### 5. update_task Tool
- **Purpose**: Modify task title or description
- **Parameters**:
  - `user_id` (string, required): User identifier
  - `task_id` (integer, required): Task identifier
  - `title` (string, optional): New title
  - `description` (string, optional): New description
- **Returns**: Object with `task_id`, `status`, and `title`

## Natural Language Commands

### Supported Commands
| User Says | Agent Should |
|-----------|--------------|
| "Add a task to buy groceries" | Call `add_task` with title "Buy groceries" |
| "Show me all my tasks" | Call `list_tasks` with status "all" |
| "What's pending?" | Call `list_tasks` with status "pending" |
| "Mark task 3 as complete" | Call `complete_task` with task_id 3 |
| "Delete the meeting task" | Call `list_tasks` first, then `delete_task` |
| "Change task 1 to 'Call mom tonight'" | Call `update_task` with new title |
| "I need to remember to pay bills" | Call `add_task` with title "Pay bills" |
| "What have I completed?" | Call `list_tasks` with status "completed" |

## Agent Behavior Specification

### Task Operations
- **Task Creation**: When user mentions adding/creating/remembering something, use `add_task`
- **Task Listing**: When user asks to see/show/list tasks, use `list_tasks` with appropriate filter
- **Task Completion**: When user says done/complete/finished, use `complete_task`
- **Task Deletion**: When user says delete/remove/cancel, use `delete_task`
- **Task Update**: When user says change/update/rename, use `update_task`

### Response Patterns
- Always confirm actions with friendly response
- Gracefully handle task not found and other errors
- Provide helpful clarifications when commands are ambiguous
- Maintain conversation context across multiple turns

## Conversation Flow (Stateless Architecture)

### Request Processing Cycle
1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server holds NO state (ready for next request)

### Benefits of Stateless Architecture
- **Scalability**: Any server instance can handle any request
- **Resilience**: Server restarts don't lose conversation state
- **Horizontal scaling**: Load balancer can route to any backend
- **Testability**: Each request is independent and reproducible

## Development Workflow

### 1. Specification Phase
- Create detailed specs in `/specs/ai/` directory
- Define agent behavior and conversation flows
- Document MCP tools and their specifications
- Use Spec-Kit Plus for structured specifications

### 2. Implementation Phase
1. Set up MCP server with task operation tools
2. Create database models for conversations and messages
3. Implement AI agent with OpenAI Agents SDK
4. Build chat API endpoint with conversation management
5. Create frontend with OpenAI ChatKit

### 3. Testing Strategy
- Unit tests for MCP tools
- Integration tests for agent-tool interactions
- Conversation flow testing
- Natural language command validation

## Resources

### references/
- `mcp_server_guide.md` - MCP server setup and tool registration
- `openai_agents_integration.md` - OpenAI Agents SDK implementation
- `conversation_management.md` - State management and persistence patterns
- `natural_language_processing.md` - NLP patterns for todo commands
- `chat_interface_patterns.md` - Chat UI and interaction patterns

### assets/
- `mcp_tool_templates/` - MCP tool definition templates
- `agent_configuration_templates/` - OpenAI agent setup templates
- `conversation_schema_templates/` - Database schema templates
- `chat_component_templates/` - Frontend chat component templates
