"""
Schémas de validation pour l'API Chat.

Ces classes définissent exactement ce que l'API accepte en entrée
et retourne en sortie. Pydantic valide automatiquement — si les données
ne correspondent pas, FastAPI retourne une erreur 422 détaillée.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timezone

class ChatRequest(BaseModel):
    """
    Ce que le frontend envoie quand l'utilisateur tape un message.
    
    Exemple JSON :
    {
        "message": "Je cherche un hôtel à Nice",
        "user_id": 1,
        "conversation_id": null       ← null = nouvelle conversation
    }
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Le message de l'utilisateur.",
    )
    
    user_id: int = Field(
        ...,
        gt=0,
        description="L'ID de l'utilisateur.",
    )
    
    conversation_id: Optional[int] = Field(
        None,
        gt=0,
        description="L'ID de la conversation existante, ou none pour une nouvelle conversation.",
    )
    
    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Le message ne peut pas être vide.')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Quelle sont les meilleures activités à Nice ?",
                "user_id": 1,
                "conversation_id": None,
            }
        }
    
class ChatResponse(BaseModel):    
    """
    Ce que l'API retourne après d'avoir traité le message.
    
    Exemple JSON :
    {
        "response": "Nice offre beaucoup d'activités...",
        "conversation_id": 42,
        "timestamp": "2024-02-01T10:30:00"
    }
    """
    response: str = Field(
        ...,
        description="La réponse du Chatbot.",
    )
    
    conversation_id: int = Field(
        ...,
        description="L'ID de la conversation.",
    )
    
    timestamp: datetime = Field(
        default_factory=lambda:datetime.now(timezone.utc),
        description="Horodatage UTC de la réponse.",
    )
    
class MessageSchema(BaseModel):
    id: int
    content: str
    is_bot: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
    
class ConversationSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    messages: list[MessageSchema] = []  # Liste des messages dans la conversation
    
    class Config:
        from_attributes = True