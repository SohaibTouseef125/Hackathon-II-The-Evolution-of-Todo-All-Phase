from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid

from models import Conversation, User


class ConversationService:
    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Conversation]:
        """Get a specific conversation by ID for a specific user"""
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        ).first()
        return conversation

    @staticmethod
    def create_conversation(session: Session, user_id: uuid.UUID) -> Conversation:
        """Create a new conversation for a user"""
        db_conversation = Conversation(
            user_id=user_id
        )

        session.add(db_conversation)
        session.commit()
        session.refresh(db_conversation)
        return db_conversation

    @staticmethod
    def get_user_conversations(session: Session, user_id: uuid.UUID) -> List[Conversation]:
        """Get all conversations for a specific user (newest first)"""
        conversations = session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        ).all()
        return conversations

    @staticmethod
    def touch_conversation(session: Session, conversation: Conversation) -> Conversation:
        """Update the conversation's updated_at timestamp"""
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def delete_conversation(session: Session, conversation: Conversation) -> bool:
        """Delete a conversation"""
        session.delete(conversation)
        session.commit()
        return True

    @staticmethod
    def get_user_latest_conversation(session: Session, user_id: uuid.UUID) -> Optional[Conversation]:
        """Get the most recently updated conversation for a user"""
        return session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        ).first()