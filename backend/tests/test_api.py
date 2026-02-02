"""
Tests de l'API Chat.
On utilise httpx pour simuler des requêtes HTTP sans serveur réel.
"""
from sqlalchemy.orm import sessionmaker, Session
import pytest
from httpx import AsyncClient, ASGITransport


from app.main import app
from app.core.database import Base, engine, SessionLocal, get_db


# ─────────────────────────────────────
# SETUP : base de données de test
# ─────────────────────────────────────

# On crée une DB séparée pour les tests (pour ne pas toucher aux données réelles)
from sqlalchemy import create_engine as ce
TEST_DATABASE_URL = "sqlite:///./test.db"  # SQLite pour les tests (pas besoin de PostgreSQL)
test_engine = ce(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

from sqlalchemy.orm import sessionmaker


def override_get_db():
    """Remplace get_db par une version qui utilise la DB de test."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Remplacer la dépendance get_db par notre version de test
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_test_db():
    """Crée les tables avant chaque test, les supprime après."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# ─────────────────────────────────────
# TESTS
# ─────────────────────────────────────

@pytest.mark.asyncio
async def test_health_check():
    """Le endpoint /health doit retourner status: healthy."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_root():
    """Le endpoint / doit retourner un message de bienvenue."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    assert "Bienvenue" in response.json()["message"]


@pytest.mark.asyncio
async def test_chat_validation_message_vide():
    """Un message vide doit être rejeté (erreur 422)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/chat", json={
            "message": "",
            "user_id": 1
        })
    
    # 422 = Unprocessable Entity (validation échouée)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_validation_user_id_negatif():
    """Un user_id négatif doit être rejeté."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/chat", json={
            "message": "Bonjour",
            "user_id": -1
        })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_validation_message_manquant():
    """Une requête sans champ 'message' doit être rejetée."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/chat", json={
            "user_id": 1
        })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_conversation_introuvable():
    """Récupérer une conversation inexistante doit retourner 404."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/conversations/9999")
    
    assert response.status_code == 404