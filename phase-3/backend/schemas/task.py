from pydantic import BaseModel
from typing import Optional
import uuid


class TaskCreateRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskListRequest(BaseModel):
    user_id: str
    status: Optional[str] = "all"  # all, pending, completed


class TaskCompleteRequest(BaseModel):
    user_id: str
    task_id: str


class TaskDeleteRequest(BaseModel):
    user_id: str
    task_id: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: list = []