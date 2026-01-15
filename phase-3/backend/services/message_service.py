from sqlmodel import Session, select
from typing import List, Optional
import uuid

from models import Message, MessageCreate


class MessageService:
    @staticmethod
    def create_message(session: Session, message_create: MessageCreate) -> Message:
        """Create a new message in a conversation"""
        db_message = Message(
            conversation_id=message_create.conversation_id,
            user_id=message_create.user_id,
            role=message_create.role,
            content=message_create.content
        )

        session.add(db_message)
        session.commit()
        session.refresh(db_message)
        return db_message

    @staticmethod
    def get_messages_by_conversation(session: Session, conversation_id: uuid.UUID) -> List[Message]:
        """Get all messages for a specific conversation ordered by creation time"""
        messages = session.exec(
            select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at)
        ).all()
        return messages

    @staticmethod
    def get_latest_messages(session: Session, conversation_id: uuid.UUID, limit: int = 10) -> List[Message]:
        """Get the latest messages for a conversation with a limit"""
        messages = session.exec(
            select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.desc()).limit(limit)
        ).all()
        # Return in chronological order (reverse the list)
        return list(reversed(messages))

    @staticmethod
    def get_message_by_id(
        session: Session,
        message_id: uuid.UUID,
        conversation_id: uuid.UUID,
    ) -> Optional[Message]:
        """Get a specific message by ID within a conversation"""
        return session.exec(
            select(Message).where(
                Message.id == message_id,
                Message.conversation_id == conversation_id,
            )
        ).first()

    @staticmethod
    def delete_message(session: Session, message: Message) -> bool:
        """Delete a single message"""
        session.delete(message)
        session.commit()
        return True

    @staticmethod
    def delete_messages_by_conversation(session: Session, conversation_id: uuid.UUID) -> int:
        """Delete all messages in a conversation (returns count deleted)"""
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()

        for msg in messages:
            session.delete(msg)

        session.commit()
        return len(messages)