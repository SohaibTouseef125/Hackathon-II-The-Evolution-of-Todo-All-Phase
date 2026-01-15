from mcp.server import Server
from mcp.types import Tool, TextContent
import sys
import os
# Add the backend directory to the Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Task, User
from db import get_session
from typing import Dict, Any, List
from datetime import datetime
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Server("todo-mcp-server")

@app.list_tools()
async def list_tools():
    """List all available tools for the todo management system."""
    return [
        Tool(
            name="add_task",
            description="Add a new task to the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (UUID string)"},
                    "title": {"type": "string", "description": "Task title (1-200 characters)"},
                    "description": {"type": "string", "description": "Optional task description (up to 1000 characters)"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for a user with optional status filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (UUID string)"},
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status: 'all', 'pending', or 'completed'",
                        "default": "all"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update an existing task's title, description, or completion status",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (UUID string)"},
                    "task_id": {"type": "string", "description": "Task ID (UUID string)"},
                    "title": {"type": "string", "description": "New task title (optional)"},
                    "description": {"type": "string", "description": "New task description (optional)"},
                    "completed": {"type": "boolean", "description": "Whether task is completed (optional)"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task from the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (UUID string)"},
                    "task_id": {"type": "string", "description": "Task ID (UUID string)"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (UUID string)"},
                    "task_id": {"type": "string", "description": "Task ID (UUID string)"}
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]):
    """
    Handle tool calls with proper validation and authentication.
    Ensures user_id matches for all operations.
    """
    try:
        # Validate user_id format
        user_id_str = arguments.get("user_id")
        if not user_id_str:
            return [TextContent(type="text", text="Error: user_id is required")]

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            return [TextContent(type="text", text="Error: Invalid user_id format. Must be a valid UUID string")]

        # Verify user exists
        with get_session() as session:
            user = session.get(User, user_id)
            if not user:
                return [TextContent(type="text", text="Error: User not found")]

        # Process the tool call
        if name == "add_task":
            return await handle_add_task(arguments, user_id)
        elif name == "list_tasks":
            return await handle_list_tasks(arguments, user_id)
        elif name == "update_task":
            return await handle_update_task(arguments, user_id)
        elif name == "delete_task":
            return await handle_delete_task(arguments, user_id)
        elif name == "complete_task":
            return await handle_complete_task(arguments, user_id)
        else:
            return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]

    except Exception as e:
        logger.error(f"Error in call_tool: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_add_task(arguments: Dict[str, Any], user_id: uuid.UUID) -> List[TextContent]:
    """Handle adding a new task."""
    try:
        title = arguments.get("title")
        description = arguments.get("description")

        # Validate required fields
        if not title:
            return [TextContent(type="text", text="Error: Title is required for creating a task")]

        # Validate title length and content
        stripped_title = title.strip()
        if len(stripped_title) < 1:
            return [TextContent(type="text", text="Error: Title cannot be empty or whitespace only")]

        if len(stripped_title) > 200:
            return [TextContent(type="text", text="Error: Title must be 1-200 characters")]

        # Validate description length if provided
        if description and len(description) > 1000:
            return [TextContent(type="text", text="Error: Description must be 1000 characters or less")]

        with get_session() as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return [TextContent(type="text", text="Error: User not found")]

            # Create new task
            task = Task(
                user_id=user_id,
                title=stripped_title,
                description=description.strip() if description else None,
                completed=False
            )

            session.add(task)
            session.commit()
            session.refresh(task)  # Refresh to get the created task details

            logger.info(f"Successfully created task '{task.title}' with ID: {task.id} for user: {user_id}")
            return [TextContent(type="text", text=f"Successfully created task '{task.title}' with ID: {task.id}")]

    except ValueError as ve:
        logger.error(f"Validation error in handle_add_task: {str(ve)}")
        return [TextContent(type="text", text=f"Validation error: {str(ve)}")]
    except Exception as e:
        logger.error(f"Error in handle_add_task: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"Error creating task: {str(e)}")]


async def handle_list_tasks(arguments: Dict[str, Any], user_id: uuid.UUID) -> List[TextContent]:
    """Handle listing tasks with optional status filtering."""
    try:
        status = arguments.get("status", "all")

        with get_session() as session:
            # Query tasks for the user
            from sqlmodel import select
            query = select(Task).where(Task.user_id == user_id)

            # Apply status filter
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)

            tasks = session.exec(query.order_by(Task.created_at.desc())).all()

            if not tasks:
                if status == "all":
                    return [TextContent(type="text", text="No tasks found for this user")]
                else:
                    return [TextContent(type="text", text=f"No {status} tasks found for this user")]

            # Format task list
            task_list = []
            for task in tasks:
                status_text = "completed" if task.completed else "pending"
                task_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": status_text,
                    "created_at": task.created_at.isoformat()
                })

            return [TextContent(type="text", text=f"Found {len(tasks)} {status} tasks:\n" +
                               "\n".join([f"- {t['id']}: {t['title']} ({t['status']})" for t in task_list]))]

    except Exception as e:
        logger.error(f"Error in handle_list_tasks: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"Error listing tasks: {str(e)}")]


async def handle_update_task(arguments: Dict[str, Any], user_id: uuid.UUID) -> List[TextContent]:
    """Handle updating an existing task."""
    try:
        task_id_str = arguments.get("task_id")
        title = arguments.get("title")
        description = arguments.get("description")
        completed = arguments.get("completed")

        # Validate task_id format
        try:
            task_id = uuid.UUID(task_id_str)
        except (ValueError, TypeError):
            return [TextContent(type="text", text="Error: Invalid task_id format. Must be a valid UUID string")]

        with get_session() as session:
            # Find the task and verify it belongs to the user
            from sqlmodel import select
            task = session.exec(select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )).first()

            if not task:
                return [TextContent(type="text", text="Error: Task not found or does not belong to this user")]

            # Validate and update fields if provided
            updates_made = []

            if title is not None:
                stripped_title = title.strip()
                if len(stripped_title) < 1:
                    return [TextContent(type="text", text="Error: Title cannot be empty")]
                if len(stripped_title) > 200:
                    return [TextContent(type="text", text="Error: Title must be 1-200 characters")]
                task.title = stripped_title
                updates_made.append(f"title to '{stripped_title}'")

            if description is not None:
                if len(description) > 1000:
                    return [TextContent(type="text", text="Error: Description must be 1000 characters or less")]
                task.description = description.strip() if description else None
                updates_made.append(f"description to '{description.strip() if description else 'None'}'")

            if completed is not None:
                task.completed = completed
                status_text = "completed" if completed else "pending"
                updates_made.append(f"status to {status_text}")

            # Update timestamp
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()

            if updates_made:
                updates_str = ", ".join(updates_made)
                logger.info(f"Successfully updated task {task.id} for user {user_id}: {updates_str}")
                return [TextContent(type="text", text=f"Successfully updated task {task.id}: {updates_str}")]
            else:
                return [TextContent(type="text", text=f"No updates were made to task {task.id}")]

    except ValueError as ve:
        logger.error(f"Validation error in handle_update_task: {str(ve)}")
        return [TextContent(type="text", text=f"Validation error: {str(ve)}")]
    except Exception as e:
        logger.error(f"Error in handle_update_task: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"Error updating task: {str(e)}")]


async def handle_delete_task(arguments: Dict[str, Any], user_id: uuid.UUID) -> List[TextContent]:
    """Handle deleting a task."""
    try:
        task_id_str = arguments.get("task_id")

        # Validate task_id format
        try:
            task_id = uuid.UUID(task_id_str)
        except (ValueError, TypeError):
            return [TextContent(type="text", text="Error: Invalid task_id format. Must be a valid UUID string")]

        with get_session() as session:
            # Find the task and verify it belongs to the user
            from sqlmodel import select
            task = session.exec(select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )).first()

            if not task:
                return [TextContent(type="text", text="Error: Task not found or does not belong to this user")]

            # Delete the task
            session.delete(task)
            session.commit()

            return [TextContent(type="text", text=f"Successfully deleted task {task.id}: {task.title}")]

    except Exception as e:
        logger.error(f"Error in handle_delete_task: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"Error deleting task: {str(e)}")]


async def handle_complete_task(arguments: Dict[str, Any], user_id: uuid.UUID) -> List[TextContent]:
    """Handle marking a task as completed."""
    try:
        task_id_str = arguments.get("task_id")

        # Validate task_id format
        try:
            task_id = uuid.UUID(task_id_str)
        except (ValueError, TypeError):
            return [TextContent(type="text", text="Error: Invalid task_id format. Must be a valid UUID string")]

        with get_session() as session:
            # Find the task and verify it belongs to the user
            from sqlmodel import select
            task = session.exec(select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )).first()

            if not task:
                return [TextContent(type="text", text="Error: Task not found or does not belong to this user")]

            # Mark as completed if not already
            if task.completed:
                return [TextContent(type="text", text=f"Task {task.id} is already completed: {task.title}")]

            task.completed = True
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()

            return [TextContent(type="text", text=f"Successfully marked task {task.id} as completed: {task.title}")]

    except Exception as e:
        logger.error(f"Error in handle_complete_task: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"Error completing task: {str(e)}")]


# For standalone server execution
if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())

    asyncio.run(main())