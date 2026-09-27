"""Authentication/authorization test endpoints (Phase 2 foundation).

`/api/users/me` — any authenticated user (student or admin).
`/api/admin/ping` — admin-only, purely to prove role-based authorization
works end-to-end. No real admin functionality is implemented here (that's
a later phase).
"""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, require_role
from app.models.user import AppUser
from app.schemas.user import AppUserResponse

router = APIRouter(tags=["auth"])


@router.get("/users/me", response_model=AppUserResponse)
def read_current_user(current_user: AppUser = Depends(get_current_user)) -> AppUser:
    """Return the authenticated CyberDesk user's application record."""
    return current_user


@router.get("/admin/ping")
def admin_ping(current_user: AppUser = Depends(require_role("admin"))) -> dict:
    """Trivial admin-only endpoint used to verify authorization works."""
    return {"message": "pong", "role": current_user.role}
