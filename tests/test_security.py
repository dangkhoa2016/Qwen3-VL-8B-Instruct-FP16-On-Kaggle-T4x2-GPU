import pytest

from qwen3vl_t4x2.config import Settings
from qwen3vl_t4x2.security import requires_public_auth, verify_bearer_token


def _settings(monkeypatch):
    monkeypatch.setenv("ENABLE_CLOUDFLARE_TUNNEL", "true")
    monkeypatch.setenv("QWEN3VL_API_KEY", "secret-key")
    return Settings.from_env()


def test_localhost_never_requires_bearer(monkeypatch):
    settings = _settings(monkeypatch)
    assert requires_public_auth("127.0.0.1:8000", settings) is False
    assert requires_public_auth("localhost:8000", settings) is False


def test_public_host_requires_bearer_when_tunnel_enabled(monkeypatch):
    settings = _settings(monkeypatch)
    assert requires_public_auth("demo.trycloudflare.com", settings) is True


def test_public_host_does_not_require_bearer_when_tunnel_disabled(monkeypatch):
    monkeypatch.setenv("ENABLE_CLOUDFLARE_TUNNEL", "false")
    monkeypatch.delenv("QWEN3VL_API_KEY", raising=False)
    settings = Settings.from_env()
    assert requires_public_auth("demo.trycloudflare.com", settings) is False


def test_verify_bearer_accepts_exact_token(monkeypatch):
    settings = _settings(monkeypatch)
    verify_bearer_token("Bearer secret-key", settings)


def test_verify_bearer_rejects_missing_or_wrong_token(monkeypatch):
    settings = _settings(monkeypatch)
    with pytest.raises(PermissionError, match="AUTH_REQUIRED"):
        verify_bearer_token(None, settings)
    with pytest.raises(PermissionError, match="AUTH_INVALID"):
        verify_bearer_token("Bearer wrong", settings)
