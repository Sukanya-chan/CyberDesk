"""Application configuration loaded from environment variables.

All configuration must come from the environment (see .env.example).
No secrets or environment-specific values are hardcoded here.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings."""

    app_name: str = "CyberDesk API"
    environment: str = "development"
    database_url: str = "sqlite:///./cyberdesk.db"

    # Comma-separated list of allowed origins for CORS, parsed in main.py.
    cors_allowed_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance.

    Cached so environment variables are read once per process rather than
    on every request.
    """
    return Settings()
