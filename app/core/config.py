from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl,PostgresDsn,field_validator
from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    
    PROJECT_NAME:str = "FastAPI APP"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A scalable, production-ready FastAPI application."
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1234"
    POSTGRES_DB: str = "app_db"
    
    
     # Async DSN built from components
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
 
    # Sync DSN for Alembic migrations
    @property
    def SYNC_DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Connection pool tuning
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
 
 
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000","https://hitchier-duane-ingenuously.ngrok-free.dev"]
    
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json | text
    
    RATE_LIMIT_PER_MINUTE: int = 60
    
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "noreply@example.com"
    EMAILS_FROM_NAME: str = "FastAPI App"
    
    
    SECRET_KEY:str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 15
    REFRESH_TOKEN_EXPIRE_DAYS:int = 7
    EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 1000
    RESET_TOKEN_EXPIRE_MINUTES: int = 15
    
    ALBIO_API_BASE_URL:str='http://127.0.0.1:8000'
    ALBIO_API_KEY:str='kgk34k0v-vkedpk349jfm340'
    
    
    
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings: Settings = get_settings()
