from datetime import datetime, timezone
from sqlalchemy.orm import Session

from db.models.chat import Chat, Message
from services.rag import rag_service


class ChatService:
    
    @classmethod
    def create_chat_message(
        cls, 
        db: Session,
        chat_id: str,
        user_message: str
    ):
        """This creates a chat message with the AI assistant reply"""
        
        # Create user message
        Message.create(
            db=db,
            content=user_message,
            chat_id=chat_id,
            role='user',
        )
        
        # Load chat history from DB (all messages before current, for RAG context)
        _, messages, _ = Message.fetch_by_field(
            db=db, paginate=False, chat_id=chat_id, order="asc"
        )
        # Exclude the current user message we just added; use previous turns as history
        chat_history = [
            (msg.role, msg.content) for msg in messages[:-1]
        ]
        
        # Generate assistant response with per-chat history
        assistant_response = rag_service.generate_answer(
            user_message, chat_history=chat_history
        )
        Message.create(
            db=db,
            content=assistant_response,
            chat_id=chat_id,
            role='assistant'
        )
        
        # Update chat last active
        Chat.update(
            db=db, id=chat_id,
            last_active_at=datetime.now(timezone.utc)
        )