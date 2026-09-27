"""Authentication and authorization tests.

Follows Clerk's documented FastAPI testing pattern: override the
`require_auth` dependency with a fake `RequestState` rather than hitting
real Clerk infrastructure or hand-rolling JWTs. This exercises our own
authorization logic (`get_current_user`, `require_role`) for real, while
treating "the token was already verified" as a given for these tests —
exactly the boundary `require_auth` itself is responsible for and that a
Clerk-side integration test would separately cover.
"""
import pytest
from clerk_backend_api.security.types import AuthStatus, RequestState
from fastapi.testclient import TestClient

from app.api.deps import require_auth
from app.db.session import Base, engine
from app.main import app

client = TestClient(app)


def _fake_state(clerk_user_id: str) -> RequestState:
    return RequestState(
        status=AuthStatus.SIGNED_IN,
        payload={"sub": clerk_user_id},
    )


@pytest.fixture(autouse=True)
def _clean_tables():
    """Reset tables between tests so user-creation tests don't interfere."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    app.dependency_overrides.pop(require_auth, None)


def test_no_token_returns_401():
    response = client.get("/api/users/me")
    assert response.status_code == 401


def test_valid_token_returns_current_user_as_student():
    app.dependency_overrides[require_auth] = lambda: _fake_state("user_student_1")

    response = client.get("/api/users/me")

    assert response.status_code == 200
    body = response.json()
    assert body["clerk_user_id"] == "user_student_1"
    assert body["role"] == "student"


def test_first_login_auto_creates_app_user_as_student():
    app.dependency_overrides[require_auth] = lambda: _fake_state("user_new_1")

    first = client.get("/api/users/me")
    second = client.get("/api/users/me")

    assert first.status_code == 200
    assert second.status_code == 200
    # Same local row both times, not a duplicate created per request.
    assert first.json()["id"] == second.json()["id"]


def test_student_cannot_access_admin_endpoint():
    app.dependency_overrides[require_auth] = lambda: _fake_state("user_student_2")

    response = client.get("/api/admin/ping")

    assert response.status_code == 403


def test_admin_can_access_admin_endpoint():
    app.dependency_overrides[require_auth] = lambda: _fake_state("user_admin_1")
    # Promote this user out-of-band, exactly as a real admin promotion
    # would happen in Phase 2 (no self-service role endpoint exists).
    client.get("/api/users/me")  # lazily creates the AppUser row as student
    from app.db.session import SessionLocal
    from app.models.user import AppUser

    db = SessionLocal()
    try:
        user = db.query(AppUser).filter(AppUser.clerk_user_id == "user_admin_1").first()
        user.role = "admin"
        db.commit()
    finally:
        db.close()

    response = client.get("/api/admin/ping")

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_health_still_public_and_unaffected_by_auth():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
