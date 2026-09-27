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
"""
import os

os.environ.setdefault("CLERK_SECRET_KEY", "sk_test_dummy_value_for_tests_only")
