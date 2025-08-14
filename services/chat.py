from sqlalchemy.orm import Session

from db.models.chat import Message
from services.rag import rag_service


class ChatService:
    
    @classmethod
    def create_chat_message(
        cls, 
        db: Session,
        user_id: str,
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
        
        # Generate assistant response
        assistant_response = rag_service.generate_answer(user_message)
        Message.create(
            db=db,
            content=assistant_response,
            chat_id=chat_id,
            role='assistant'
        )