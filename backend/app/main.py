from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.api import chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === DÉMARRAGE ===
    print("🚀 Démarrage de TravelBot..")
    init_db()
    print(f"🌐 Serveur démarré sur l'URL: http://{settings.host}:{settings.port}")
    print(f"📚 Swagger disponible sur l'URL: http://localhost:{settings.port}/docs")
    
    yield
    
    # === ARRÊT ===
    print("🛑 Arrêt de TravelBot..")
    

app = FastAPI(
    title=settings.app_name,
    description="Un chatbot touristique propulsé par OpenAI et LangChain.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middlewar(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Monter les routes ---
app.include_router(
    chat.router,
    prefix="/api",
    tags=["Chat"]
)

# --- Routes utilitaires ---
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name
    }

@app.get("/")
async def root():
    return {
        "message": f"Bienvenue sur l'API {settings.app_name}!",
        "docs":"/docs",
        "health":"/health"
    }
    
# --- Lancement direct ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )