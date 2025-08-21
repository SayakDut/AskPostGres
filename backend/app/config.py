"""
Configuration settings for AskPostgres backend application.
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database settings
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    postgres_db: str = Field(env="POSTGRES_DB")
    postgres_user: str = Field(env="POSTGRES_USER")
    postgres_password: str = Field(env="POSTGRES_PASSWORD")
    
    # OpenRouter API settings
    openrouter_api_key: str = Field(env="OPENROUTER_API_KEY")
    
    # Application settings
    site_url: str = Field(default="http://localhost:3000", env="SITE_URL")
    site_name: str = Field(default="AskPostgres", env="SITE_NAME")
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    
    # Security settings
    secret_key: str = Field(env="SECRET_KEY")
    allowed_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000", 
        env="ALLOWED_ORIGINS"
    )
    
    # Rate limiting
    redis_url: str = Field(default="", env="REDIS_URL")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse allowed origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
