"""Response schemas for the authenticated user."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppUserResponse(BaseModel):
    """What `/api/users/me` returns. No Clerk profile data (email, name)
    is included here — CyberDesk's backend doesn't store it (see
    context/Decisions.md ADR-006/ADR-007)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    clerk_user_id: str
    role: str
    created_at: datetime
    updated_at: datetime
