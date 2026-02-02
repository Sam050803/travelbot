"""
Service LangChain : tout ce qui concerne l'IA.
Gère la configuration du modèle, le prompt, la mémoire, et les appels à OpenAI.
"""

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List, Dict

from app.core.config import settings

# ─────────────────────────────────────
# PROMPT SYSTÈME : la "personnalité" du bot
# ─────────────────────────────────────
# Ce texte est envoyé à chaque requête comme contexte de base.
# Il définit comment le bot doit se comporter.
TRAVELBOT_SYSTEM_PROMPT = """
Tu es TravelBot, un assistant touristique intelligent et enthousiaste.

PERSONNALITÉ :
- Chaleureux et accueillant
- Expert en tourisme et voyage
- Pratique et orienté solutions
- Toujours positif

RÈGLES :
1. Réponds TOUJOURS en français
2. Donne des recommandations personnalisées basées sur le contexte
3. Inclus des détails pratiques (prix indicatifs, horaires, moyens de transport)
4. Si tu ne sais pas quelque chose, dis-le honnêtement
5. Reste concis (2-3 paragraphes max par réponse)

SPÉCIALITÉS :
- Activités touristiques et loisirs
- Restaurants et gastronomie locale
- Hébergements (hôtels, locations)
- Transport et itinéraires
- Événements culturels
- Conseils pratiques de voyage

STYLE :
- Utilise des emojis occasionnellement (🏖️ 🍽️ 🎭)
- Pose des questions de clarification si nécessaire
- Propose des alternatives

Ton objectif : Aider le voyageur à profiter au maximum de son expérience !
"""

class LangChainService:
    """
    Orchestre les appels à OpenAI via LangChain.
    """
    def __init__(self):
        # Le modèle OpenAI — temperature contrôle la créativité
        # 0.0 = très déterministe, 1.0 = très créatif
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.openai_temperature,
            openai_api_key=settings.openai_api_key,
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", TRAVELBOT_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
    def create_conversation_chain(self, memory_type: str = "buffer") -> ConversationChain:
        if memory_type == "buffer":
            memory = ConversationBufferMemory(
                return_messages=True,
                memory_key="history"
            )
        elif memory_type == "window":
            from langchain.memory import ConversationBufferWindowMemory
            memory = ConversationBufferWindowMemory(
                k=10,
                return_messages=True,
                memory_key="history"
            )
        else:
            from langchain.memory import ConversationSummaryMemory
            memory = ConversationSummaryMemory(
                llm=self.llm,
                return_messages=True,
                memory_key="history"
            )
            
        return ConversationChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=memory,
            verbose=settings.debug,
        )
        
    def load_history_into_memory(self, conversation:ConversationChain, history: List[Dict[str, str]]):
        """
        Charge l'historique depuis la DB dans la mémoire LangChain.
        
        history = [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]
        """
        for message in history:
            if message["role"]=="user":
                conversation.memory.chat_memory.add_user_message(message["content"])
            elif message["role"]=="assistant":
                conversation.memory.chat_memory.add_ai_message(message["content"])
    
    async def get_response(self, message:str, conversation_history: List[Dict[str, str]]=None) -> str:
        """
        Obtient une réponse du bot pour un message donné et un historique.
        """
        conversation = self.create_conversation_chain()
        
        if conversation_history:
            self.load_history_into_memory(conversation, conversation_history)
        
        response = await conversation.apredict(input=message)
        
        return response
        