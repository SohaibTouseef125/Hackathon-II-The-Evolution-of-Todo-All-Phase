from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional

from models import Conversation, ConversationRead, Message, MessageRead, UserRead
from db import get_session
from auth import get_current_user
from agents.runner import agent_runner
from services.conversation_service import ConversationService
from services.message_service import MessageService
import json
from sqlmodel import select
import uuid

router = APIRouter()

import time
import logging

logger = logging.getLogger(__name__)


def _ensure_user_access(user_id: str, current_user: UserRead) -> uuid.UUID:
    """Validate user access and return parsed UUID."""
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's data",
        )

    try:
        return uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid user_id format",
        )


def _parse_uuid(value: str, field_name: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid {field_name} format",
        )


def _to_conversation_read(conv: Conversation) -> ConversationRead:
    return ConversationRead(
        id=conv.id,
        user_id=conv.user_id,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
    )


def _to_message_read(msg: Message) -> MessageRead:
    return MessageRead(
        id=msg.id,
        conversation_id=msg.conversation_id,
        user_id=msg.user_id,
        role=msg.role,
        content=msg.content,
        created_at=msg.created_at,
        tool_calls=msg.tool_calls,
    )


@router.get("/{user_id}/conversations", response_model=List[ConversationRead])
def list_conversations(
    user_id: str,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user_uuid = _ensure_user_access(user_id, current_user)
    conversations = ConversationService.get_user_conversations(db, user_uuid)
    return [_to_conversation_read(c) for c in conversations]


@router.post("/{user_id}/conversations", response_model=ConversationRead)
def create_conversation(
    user_id: str,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user_uuid = _ensure_user_access(user_id, current_user)
    conv = ConversationService.create_conversation(db, user_uuid)
    return _to_conversation_read(conv)


@router.get("/{user_id}/conversations/latest", response_model=Optional[ConversationRead])
def get_latest_conversation(
    user_id: str,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user_uuid = _ensure_user_access(user_id, current_user)
    conv = ConversationService.get_user_latest_conversation(db, user_uuid)
    return _to_conversation_read(conv) if conv else None


@router.get("/{user_id}/conversations/{conversation_id}/messages", response_model=List[MessageRead])
def get_conversation_messages(
    user_id: str,
    conversation_id: str,
    limit: Optional[int] = Query(default=None, ge=1, le=500),
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user_uuid = _ensure_user_access(user_id, current_user)
    conv_uuid = _parse_uuid(conversation_id, "conversation_id")

    conversation = ConversationService.get_conversation_by_id(db, conv_uuid, user_uuid)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if limit is None:
        msgs = MessageService.get_messages_by_conversation(db, conversation.id)
    else:
        msgs = MessageService.get_latest_messages(db, conversation.id, limit=limit)

    return [_to_message_read(m) for m in msgs]


@router.delete("/{user_id}/conversations/{conversation_id}")
def delete_conversation(
    user_id: str,
    conversation_id: str,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user_uuid = _ensure_user_access(user_id, current_user)
    conv_uuid = _parse_uuid(conversation_id, "conversation_id")

    conversation = ConversationService.get_conversation_by_id(db, conv_uuid, user_uuid)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    # Delete messages first to avoid foreign key issues
    MessageService.delete_messages_by_conversation(db, conversation.id)
    ConversationService.delete_conversation(db, conversation)
    return {"message": "Conversation deleted"}


@router.delete("/{user_id}/conversations/{conversation_id}/messages")
def clear_conversation_messages(
    user_id: str,
    conversation_id: str,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user_uuid = _ensure_user_access(user_id, current_user)
    conv_uuid = _parse_uuid(conversation_id, "conversation_id")

    conversation = ConversationService.get_conversation_by_id(db, conv_uuid, user_uuid)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    deleted_count = MessageService.delete_messages_by_conversation(db, conversation.id)
    ConversationService.touch_conversation(db, conversation)
    return {"message": "Conversation cleared", "deleted": deleted_count}


@router.delete("/{user_id}/conversations/{conversation_id}/messages/{message_id}")
def delete_message(
    user_id: str,
    conversation_id: str,
    message_id: str,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user_uuid = _ensure_user_access(user_id, current_user)
    conv_uuid = _parse_uuid(conversation_id, "conversation_id")
    msg_uuid = _parse_uuid(message_id, "message_id")

    conversation = ConversationService.get_conversation_by_id(db, conv_uuid, user_uuid)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    msg = MessageService.get_message_by_id(db, msg_uuid, conversation.id)
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    MessageService.delete_message(db, msg)
    ConversationService.touch_conversation(db, conversation)
    return {"message": "Message deleted"}

@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    message: Dict[str, Any],
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Chat endpoint that processes user messages and returns AI responses.
    This endpoint integrates with the AI agent and MCP tools to handle todo operations.
    """
    start_time = time.time()

    try:
        user_uuid = _ensure_user_access(user_id, current_user)

        # Validate input message
        user_message = message.get("message", "")
        if not user_message or not isinstance(user_message, str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Message is required and must be a string"
            )

        # Sanitize user input to prevent prompt injection
        # Remove any potential system message indicators
        sanitized_message = user_message.replace("System:", "").replace("system:", "")

        conversation_id = message.get("conversation_id")

        # Get or create conversation
        conversation = None
        if conversation_id:
            try:
                # Look for existing conversation for this user
                statement = select(Conversation).where(
                    Conversation.id == uuid.UUID(conversation_id),
                    Conversation.user_id == user_uuid
                )
                conversation = db.exec(statement).first()
            except ValueError:
                # Invalid UUID format
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid conversation_id format"
                )

        if not conversation:
            # Create new conversation
            conversation = Conversation(user_id=user_uuid)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Fetch conversation history for context
        conversation_history = []
        statement = select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at)
        messages = db.exec(statement).all()

        for msg in messages:
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Process the message using the agent runner
        result = await agent_runner.run_conversation(
            user_id=user_id,
            message=sanitized_message,
            conversation_history=conversation_history
        )

        # Store user message in conversation
        user_msg = Message(
            conversation_id=conversation.id,
            user_id=user_uuid,
            role="user",
            content=sanitized_message
        )
        db.add(user_msg)

        # Store assistant response in conversation
        assistant_msg = Message(
            conversation_id=conversation.id,
            user_id=user_uuid,
            role="assistant",
            content=result.get("response", ""),
            tool_calls=json.dumps(result.get("tool_calls", [])) if result.get("tool_calls") else None
        )
        db.add(assistant_msg)

        # Commit both messages to database
        db.commit()

        # Touch conversation (so it sorts to top in history)
        ConversationService.touch_conversation(db, conversation)

        # Calculate and log performance metrics
        processing_time = time.time() - start_time
        logger.info(f"Chat endpoint processing completed for user {user_id} in {processing_time:.2f}s")

        return {
            "conversation_id": str(conversation.id),
            "response": result.get("response", ""),
            "tool_calls": result.get("tool_calls", [])
        }
    except HTTPException:
        # Calculate and log performance metrics even for HTTP exceptions
        processing_time = time.time() - start_time
        logger.info(f"Chat endpoint processing failed for user {user_id} in {processing_time:.2f}s")
        # Re-raise HTTP exceptions to preserve status codes
        raise
    except Exception as e:
        # Calculate and log performance metrics for unexpected errors
        processing_time = time.time() - start_time
        logger.info(f"Chat endpoint processing failed for user {user_id} in {processing_time:.2f}s")
        # Log the error and return a generic error response
        logger.error(f"Unexpected error in chat endpoint for user {user_id}: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while processing your request"
        )