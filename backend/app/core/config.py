from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "backend":
    PROJECT_ROOT = PROJECT_ROOT.parent

BACKEND_ROOT = PROJECT_ROOT / "backend"

class Settings(BaseSettings):
    app_name: str = "CyberDesk API"
    environment: str = "development"
    database_url: str = "sqlite:///" + str(BACKEND_ROOT / "cyberdesk.db")
    cors_allowed_origins: str = 'http://localhost:5173'
    clerk_secret_key: str = ""
    clerk_jwt_key: str = ""
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    frontend_url: str = 'http://localhost:5173'
    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
