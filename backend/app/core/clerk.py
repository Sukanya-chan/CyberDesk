"""Clerk backend client configuration.

Wraps the official `clerk-backend-api` SDK client so the rest of the
backend never touches the secret key or SDK construction directly.
"""
from functools import lru_cache

from clerk_backend_api import Clerk

from app.core.config import get_settings


@lru_cache
def get_clerk_client() -> Clerk:
    """Return a cached Clerk SDK client configured from the environment."""
    settings = get_settings()
    if not settings.clerk_secret_key:
        raise RuntimeError(
            "CLERK_SECRET_KEY is not set. Copy backend/.env.example to "
            "backend/.env and fill in your Clerk secret key."
        )
    return Clerk(bearer_auth=settings.clerk_secret_key)
