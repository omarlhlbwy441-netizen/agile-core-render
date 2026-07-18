from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AGILE Core System"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Agile Project Management API"

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/agile"
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
