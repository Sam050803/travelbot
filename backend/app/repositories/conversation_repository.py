from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import Conversation, Message, User

class ConversationRepository:
    """Repository pour gérer toutes opératons liées aux conversations et messages."""
    
    def __init__(self, db: Session):
        self.db = db
        
    def create_conversation(self, user_id:int, client_id: int =1)-> Conversation:
        """Créer une nouvelle conversation pour un utilisateur."""
        conversation = Conversation(user_id=user_id, client_id=client_id)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Retourne une conversation par son ID ou None si elle n'existe pas."""
        return self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
    def get_user_conversations(self, user_id: int, limit: int = 10) -> List[Conversation]:
        """Retourne les conversations d'un utilisateur, les plus récentes en premier."""
        return self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(
            Conversation.created_at.desc()
        ).limit(limit).all()
        
    def delete_coversation(self, conversation_id: int)-> bool:
        """Supprime une conversation (et ses messages via CASCADE). Retourne True si succès."""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return False
        self.db.delete(conversation)
        self.db.commit()
        return True
    
    def add_message(self, conversation_id: int, content: str, is_bot: bool=False)-> Message:
        """Ajoute un message à une conversation."""
        message = Message(
            conversation_id=conversation_id,
            content=content,
            is_bot=is_bot
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_messages(self, conversation_id:int, limit: int=50) -> List[Message]:
        """Retourne les messages d'une conversation en ordre chronologique."""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(
            Message.created_at.asc()
        ).limit(limit).all()
        
    def get_conversation_history(self, conversation_id:int, limit: int=10)->List[dict]:
        """Retourne l'historique au format que LangChain comprend.
        Exemple :
        [
            {"role": "user", "content": "Bonjour"},
            {"role": "assistant", "content": "Salut! Comment puis-je vous aider?"}
        ]
        """
        messages = self.get_messages(conversation_id, limit=limit)
        return [
            {
                "role": "assistant" if msg.is_bot else "user",
                "content": msg.content
            }
            for msg in messages
        ]
        
    def get_or_create_user(self, email:str, name: str="Utilisateur") -> User:
        """Retourne un utilisateur existant par email ou en crée un nouveau."""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email, name=name)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user