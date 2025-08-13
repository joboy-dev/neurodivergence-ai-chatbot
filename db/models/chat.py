import sqlalchemy as sa
from sqlalchemy import event, update
from sqlalchemy.orm import relationship, Session

from db.models.base import BaseTableModel


class Chat(BaseTableModel):
    __tablename__ = "chats"

    name = sa.Column(sa.String(255), nullable=True, index=True)
    last_message = sa.Column(sa.Text, nullable=True)
    last_active_at = sa.Column(sa.DateTime(timezone=True), nullable=True)

    user_id = sa.Column(sa.String, sa.ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", backref="chats", uselist=False)
    

class Message(BaseTableModel):
    __tablename__ = "messages"

    content = sa.Column(sa.Text, nullable=False)
    chat_id = sa.Column(sa.String, sa.ForeignKey("chats.id"), nullable=False, index=True)
    user_id = sa.Column(sa.String, nullable=False, index=True)  # -1 for the AI assistant
    
    chat = relationship("Chat", backref="messages", uselist=False)
    user = relationship(
        "User", 
        backref="messages", 
        primaryjoin="User.id == foreign(Message.user_id)",
        uselist=False
    )
