from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Travelbot"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    database_url: str
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.7
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }

settings = Settings()

def get_settings() -> Settings:
    return settings