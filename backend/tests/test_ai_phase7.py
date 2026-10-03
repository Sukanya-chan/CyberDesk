import pytest
from app.core.config import get_settings
from app.services.ai import AIError

def test_ai_is_optional_by_default(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")
    get_settings.cache_clear()
    assert get_settings().gemini_api_key == ""

def test_ai_error_contract():
    err = AIError(503, "not configured")
    assert err.status_code == 503
    assert err.message == "not configured"
