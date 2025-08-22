"""
Configuration settings for AskPostgres application.
"""
import os
from typing import List, Optional
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
    site_url: str = Field(default="http://localhost:8501", env="SITE_URL")
    site_name: str = Field(default="AskPostgres", env="SITE_NAME")
    
    # API settings (for FastAPI backend if needed)
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    
    # Security settings
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    
    # Rate limiting
    max_requests_per_minute: int = Field(default=30, env="MAX_REQUESTS_PER_MINUTE")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Streamlit settings
    streamlit_theme: str = Field(default="light", env="STREAMLIT_THEME")
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def sync_database_url(self) -> str:
        """Construct synchronous PostgreSQL database URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    def validate_required_settings(self) -> List[str]:
        """Validate that all required settings are present."""
        errors = []
        
        required_fields = [
            ("POSTGRES_DB", self.postgres_db),
            ("POSTGRES_USER", self.postgres_user),
            ("POSTGRES_PASSWORD", self.postgres_password),
            ("OPENROUTER_API_KEY", self.openrouter_api_key),
        ]
        
        for field_name, field_value in required_fields:
            if not field_value or field_value.startswith("your_"):
                errors.append(f"Missing or invalid {field_name}")
        
        return errors
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
