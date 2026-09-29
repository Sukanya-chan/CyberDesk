"""Shared pytest fixtures.

Sets a dummy CLERK_SECRET_KEY before anything imports app.main, so that
tests exercising the real (non-overridden) `require_auth` path — e.g. "no
token supplied" -> 401 — hit Clerk's own "missing token" check rather
than our own "you forgot to configure this deployment" guard. This value
is never sent anywhere; `authenticate_request()` with no token on the
request never reaches signature verification, so its validity doesn't
matter for that path. Tests that need actual signature verification
should override `require_auth` instead (see test_auth.py), not rely on
this value being real.

Also points DATABASE_URL at an isolated, throwaway SQLite file *before*
anything imports app.db.session or app.main. `Settings.database_url`
defaults to "sqlite:///./cyberdesk.db" (the real development database),
and `app/db/session.py` reads it once at import time via a module-level
`get_settings()` call — so this env var must be set here, in conftest,
which pytest loads before collecting any test module, and must never be
set with `setdefault` (a real developer .env must not silently win).
Tests must NEVER touch the development database.
"""
import atexit
import os
import tempfile

_TEST_DB_FD, _TEST_DB_PATH = tempfile.mkstemp(prefix="cyberdesk_test_", suffix=".db")
os.close(_TEST_DB_FD)

# Overwrite unconditionally: a developer's real backend/.env (which sets
# DATABASE_URL=sqlite:///./cyberdesk.db) must never leak into the test run.
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB_PATH}"
os.environ.setdefault("CLERK_SECRET_KEY", "sk_test_dummy_value_for_tests_only")


@atexit.register
def _cleanup_test_db() -> None:
    """Remove the throwaway test database file when the test process exits."""
    try:
        os.remove(_TEST_DB_PATH)
    except OSError:
        pass
