# Model Message - représente un message dans une conversation entre un utilisateur et le chatbot.

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    
    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id", ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    content = Column(
        Text, # Text au lieu de String pour les longs messages
        nullable=False,
    )
    
    # Indique si le message a été envoyé par le bot ou l'utilisateur
    is_bot = Column(
        Boolean,
        default=False,
        nullable=False
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    
    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )
    
    def __repr__(self):
        sender = "Bot" if self.is_bot else "User"
        preview = (self.content[:50] + '...') if len(self.content) > 50 else self.content
        return f"<Message({sender}: {preview})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "content": self.content,
            "is_bot": self.is_bot,
            "created_at": self.created_at.isoformat()
        }
    