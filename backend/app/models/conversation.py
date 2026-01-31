# Model Conversation - représente une conversation entre un utilisateur et le chatbot.
# Chaque conversation peut contenir plusieurs messages.

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id =  Column(Integer, primary_key=True, index=True)
    
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    client_id = Column(
        Integer,
        nullable=False,
        default=1,
        index=True
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    user = relationship(
        "User",
        back_populates="conversations",
    )
    
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by= "Message.created_at",
        lazy="dynamic"
    )
    
    def __repr__(self):
        return f"<Conversation id={self.id} user_id={self.user_id}>"
    
    def to_dict(self, include_messages=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "client_id": self.client_id,
            "created_at": self.created_at.isoformat(),
        }
        if include_messages:
            data["messages"] = [msg.to_dict() for msg in self.messages]
        return data