---
name: mcp-server-python
description: Official Model Context Protocol (MCP) Python SDK for building MCP servers. Use when exposing application functionality as tools that AI agents can invoke, including task CRUD operations for the todo app.
---

# MCP Python SDK

Build MCP servers that expose your application functionality as tools for AI agents.

## Installation

```bash
pip install mcp
```

## Basic Server Structure

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("todo-mcp-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_task",
            description="Add a new task to the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"}
                },
                "required": ["user_id", "title"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add_task":
        # Implement task creation logic
        task = create_task(arguments["user_id"], arguments["title"], arguments.get("description"))
        return [TextContent(type="text", text=f"Task created: {task.id}")]
    # Handle other tools...
```

## Todo App MCP Tools

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from models import Task

app = Server("todo-mcp-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_task",
            description="Create a new task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string", "description": "Task title (1-200 chars)"},
                    "description": {"type": "string", "description": "Optional description"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List user's tasks with optional filtering",
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
                    "task_id": {"type": "integer", "description": "Task ID"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task from the list",
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
    user_id = arguments["user_id"]

    if name == "add_task":
        task = Task(
            user_id=user_id,
            title=arguments["title"],
            description=arguments.get("description")
        )
        db.session.add(task)
        db.session.commit()
        return [TextContent(type="text", text=f"Created task {task.id}: {task.title}")]

    elif name == "list_tasks":
        query = db.session.query(Task).filter(Task.user_id == user_id)
        if arguments.get("status") == "pending":
            query = query.filter(Task.completed == False)
        elif arguments.get("status") == "completed":
            query = query.filter(Task.completed == True)
        tasks = query.all()
        return [TextContent(type="text", text=str([t.__dict__ for t in tasks]))]

    elif name == "complete_task":
        task = db.session.query(Task).filter(
            Task.id == arguments["task_id"],
            Task.user_id == user_id
        ).first()
        if task:
            task.completed = True
            db.session.commit()
            return [TextContent(type="text", text=f"Completed task {task.id}")]
        return [TextContent(type="text", text="Task not found")]

    # Similar handlers for delete_task, update_task...
```

## Running the MCP Server

```python
from mcp.server.stdio import stdio_server

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Integration with FastAPI

```python
from mcp.server.fastapi import create_app
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # Start MCP server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream.write_stream, app.create_initialization_options())

fastapi_app = create_app(app)
```

## See Also

- [OpenAI Agents SDK Skill](../openai-agents-sdk/SKILL.md) - For agents using MCP tools
- [Phase 3 Todo Chatbot Skill](../phase3-todo-chatbot/SKILL.md) - Complete implementation
- [Stateless Chatbot Architecture](../stateless-chatbot-architecture/SKILL.md) - Request cycle pattern
