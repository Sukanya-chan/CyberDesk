"""Authentication and authorization dependencies.

These are deliberately kept as two separate layers, per the Phase 2
architecture decision:

- Authentication ("who is this?") is `require_auth`: it verifies the
  Clerk-issued session token and returns Clerk's own `RequestState`. It
  knows nothing about CyberDesk roles.
- Authorization ("what can they do?") is `get_current_user` +
  `require_role`: it maps the verified Clerk identity to our local
  `AppUser` row and checks its `role`. It never trusts anything the
  client supplies directly — the role always comes from our own database,
  looked up by the Clerk user ID taken from the verified token.
"""
from typing import Annotated

from clerk_backend_api import AuthenticateRequestOptions, authenticate_request
from clerk_backend_api.security.types import RequestState
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.models.user import AppUser

# auto_error=False so Clerk's own rejection reasons (missing vs. invalid
# token) surface instead of a generic FastAPI 403; also gives the Swagger
# UI an "Authorize" button.
_http_bearer = HTTPBearer(auto_error=False)


def require_auth(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
    _creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_http_bearer)] = None,
) -> RequestState:
    """Verify the incoming Clerk session token. Authentication only.

    Raises 401 if no token was supplied or the token is invalid/expired.
    Never inspects or trusts any role/user-id the client may have also
    sent in headers or the body — only the verified token's claims count.
    """
    if not settings.clerk_secret_key:
        # Fails loudly and clearly rather than letting the Clerk SDK raise
        # an opaque internal error for a misconfigured deployment.
        raise RuntimeError(
            "CLERK_SECRET_KEY is not set. Copy backend/.env.example to "
            "backend/.env and fill in your Clerk secret key."
        )

    authorized_parties = [
        origin.strip() for origin in settings.cors_allowed_origins.split(",") if origin.strip()
    ]

    state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=settings.clerk_secret_key,
            jwt_key=settings.clerk_jwt_key or None,
            authorized_parties=authorized_parties,
            accepts_token=["session_token"],
        ),
    )

    if not state.is_signed_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=state.reason.name if state.reason else "unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return state


def get_current_user(
    auth_state: Annotated[RequestState, Depends(require_auth)],
    db: Session = Depends(get_db),
) -> AppUser:
    """Resolve the verified Clerk identity to a local AppUser row.

    The Clerk user ID comes only from `auth_state.payload["sub"]` — i.e.
    from the cryptographically verified token, never from a client-
    supplied header, query param, or body field. If this is the first
    time this Clerk user has been seen, a local row is created with the
    default role "student" (ADR-008); there is no client-controlled way
    to set a different initial role.
    """
    clerk_user_id = auth_state.payload["sub"]

    user = db.query(AppUser).filter(AppUser.clerk_user_id == clerk_user_id).first()
    if user is None:
        user = AppUser(clerk_user_id=clerk_user_id, role="student")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def require_role(required_role: str):
    """Return a dependency that authorizes only users with the given role.

    Raises 403 (not 401 — the user IS authenticated, just not permitted)
    when `current_user.role` doesn't match. The role is read exclusively
    from the AppUser row resolved above; nothing from the request itself
    can influence this check.
    """

    def _check(current_user: Annotated[AppUser, Depends(get_current_user)]) -> AppUser:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"requires role: {required_role}",
            )
        return current_user

    return _check
