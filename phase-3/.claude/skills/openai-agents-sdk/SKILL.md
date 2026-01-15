---
name: openai-agents-sdk
description: OpenAI Agents SDK for building AI agents with tool calling support. Use when implementing agentic AI behavior, including agent/runner patterns, tool integration, and handoffs between agents.
---

# OpenAI Agents SDK

The OpenAI Agents SDK enables building sophisticated AI agents that can use tools, make decisions, and hand off to specialized agents.

## Core Concepts

### Agent and Runner

```python
from agents import Agent, Runner

# Define an agent with instructions and tools
todo_agent = Agent(
    name="Todo Agent",
    instructions="You are a helpful assistant for managing todos. Help users add, list, update, and complete tasks.",
    tools=[add_task, list_tasks, complete_task, update_task, delete_task]
)

# Run the agent with user input
result = Runner.run(todo_agent, input="Add a task to buy groceries")
print(result.final_output)
```

### Handoffs

Transfer control between specialized agents:

```python
from agents import Agent, Runner

# Create specialized agents
scheduler_agent = Agent(
    name="Scheduler",
    instructions="You help users schedule and set reminders for tasks.",
    tools=[set_reminder]
)

todo_agent = Agent(
    name="Todo Agent",
    instructions="You help users manage todos. If user wants scheduling, handoff to Scheduler agent.",
    handoffs=[scheduler_agent]
)
```

### Model Configuration

```python
from agents import Agent, ModelSettings

agent = Agent(
    name="Task Agent",
    instructions="Manage user tasks.",
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2,
        max_tokens=1000,
        truncation_strategy="auto"
    )
)
```

## Streaming Responses

```python
from agents import Runner
import asyncio

async def stream_response():
    async for event in Runner.run_streamed(todo_agent, input="List all my tasks"):
        if event.type == "raw_response_event":
            print(event.data, end="", flush=True)

asyncio.run(stream_response())
```

## Error Handling

```python
from agents import Agent, Runner, RetryError

try:
    result = Runner.run(todo_agent, input="Complex task")
except RetryError:
    print("Agent failed after retries")
except Exception as e:
    print(f"Error: {e}")
```

## See Also

- [MCP Server Python Skill](../mcp-server-python/SKILL.md) - For exposing tools via MCP
- [Phase 3 Todo Chatbot Skill](../phase3-todo-chatbot/SKILL.md) - Complete implementation
- [Stateless Chatbot Architecture](../stateless-chatbot-architecture/SKILL.md) - Request cycle pattern
