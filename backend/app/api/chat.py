"""
Routes API du chat.
C'est ici que les requêtes HTTP arrivent et sont traitées.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot_service import ChatbotService

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    try:
        service = ChatbotService(db)
        
        bot_response, conversation_id = await service.process_message(
            user_id=request.user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            bot_response=bot_response,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        print(f"❌ Erreur /api/chat : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur est survenue lors du traitement du message: {str(e)}"
        )
@router.get("/conversations/{conversation_id}")       
async def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    try:
        service  = ChatbotService(db)
        messages = service.get_conversation_messages(conversation_id)
        
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {conversation_id} non trouvée."
            )
        
        return {
            "conversation_id": conversation_id,
            "messages": messages
        }

    except HTTPException as e:
        print(f"❌ Erreur /api/conversations/{conversation_id} : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )