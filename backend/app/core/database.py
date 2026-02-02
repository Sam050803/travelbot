from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping= True,
    pool_size = 10,
    max_overflow=20,
    echo=settings.debug,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def init_db() -> None:
    from app.models import user, conversation, message
    from app.models.user import User
    
    Base.metadata.create_all(bind=engine)
    
    # Créer un utilisateur de démo si aucun n'existe
    db = SessionLocal()
    try:
        existing_user = db.query(User).first()
        if not existing_user:
            demo_user = User(email="demo@travelbot.local", name="Utilisateur Demo")
            db.add(demo_user)
            db.commit()
            print("👤 Utilisateur de démo créé (id=1)")
    finally:
        db.close()
    
    print("*******Base de données initialisée*******")