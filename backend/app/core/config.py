from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Travelbot"
    debug: bool = False
    database_url: str
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()

def get_settings() -> Settings:
    return settings