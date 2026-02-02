"""
Service Chatbot : orchestre le flux complet d'un message.

Quand un utilisateur envoie un message, voici ce qui se passe :
1. On récupère (ou on crée) la conversation en DB
2. On sauvegarde le message de l'utilisateur
3. On récupère l'historique depuis la DB
4. On l'envoie à LangChain pour obtenir une réponse
5. On sauvegarde la réponse du bot
6. On retourne la réponse au frontend
"""

from sqlalchemy.orm import Session
from typing import Tuple

from app.services.langchain_service import LangChainService
from app.repositories.conversation_repository import ConversationRepository

class ChatbotService:
    
    def __init__(self, db: Session):
        self.conversation_repository = ConversationRepository(db)
        self.langchain_service = LangChainService()
        
    async def process_message(
        self,
        user_id: int,
        message: str,
        conversation_id: int = None
    )-> Tuple[str, int]:
        """
        Traite un message utilisateur et retourne la réponse du bot et l'ID de la conversation.
        """
        # 1. Créer ou récupérer la conversation
        if conversation_id:
            conversation = self.conversation_repository.get_conversation(conversation_id)
            if not conversation:
                conversation = self.conversation_repository.create_conversation(user_id)
        else:
            conversation = self.conversation_repository.create_conversation(user_id)
            
        # 2. Sauvegarder le message utilisateur
        self.conversation_repository.add_message(
            conversation_id=conversation.id,
            content=message,
           is_bot=False
        )
        
        # 3. Récupérer l'historique des messages
        history = self.conversation_repository.get_conversation_history(
            conversation.id, 
            limit=10
        )
        
        # 4. Obtenir une réponse de l'IA
        bot_response = self.langchain_service.get_response(
            message=message, 
            conversation_history=history
        )
        
        # 5. Sauvegarder la réponse du bot
        self.conversation_repository.add_message(
            message=bot_response,
            conversation_id=conversation.id,
            is_bot=True
        )
        
        # 6. Retourner la réponse et l'ID de la conversation
        return bot_response, conversation.id
    
    def get_conversation_messages(self, conversation_id: int):
        
        return self.conversation_repository.get_conversation_messages(conversation_id)