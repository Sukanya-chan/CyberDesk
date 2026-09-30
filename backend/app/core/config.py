"""Application configuration loaded from environment variables.

All configuration must come from the environment (see .env.example).
No secrets or environment-specific values are hardcoded here.
"""
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings."""

    app_name: str = "CyberDesk API"
    environment: str = "development"
    database_url: str = "sqlite:///./cyberdesk.db"

    # Comma-separated list of allowed origins for CORS, parsed in main.py.
    cors_allowed_origins: str = "http://localhost:5173"

    # Clerk (Phase 2). CLERK_SECRET_KEY must never be exposed to the
    # frontend. No default is provided — an empty value is caught
    # explicitly where it's used so misconfiguration fails loudly.
    #
    # CLERK_JWT_KEY (the PEM public key from the Clerk Dashboard) enables
    # fast, networkless local signature verification. It's optional: if
    # left unset, the SDK falls back to fetching Clerk's JWKS over the
    # network and caching it in memory.
    clerk_secret_key: str = ""
    clerk_jwt_key: str = ""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
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
