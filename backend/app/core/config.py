"""Configuration settings for the application."""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Database - Use SQLite for local development
    postgres_url: str = "sqlite:///./habitloop.db"
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "https://segnimekonnen7.github.io"]
    
    # Email
    sendgrid_api_key: Optional[str] = None
    alerts_from_email: str = "alerts@habitloop.local"
    app_base_url: str = "http://localhost:3000"
    
    # Auth
    jwt_secret: str = "please-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # Scheduler
    scheduler_interval_minutes: int = 15
    
    # Bandit
    bandit_epsilon: float = 0.1
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
