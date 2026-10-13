from pathlib import Path

import pytest

from qwen3vl_t4x2.config import Settings


def test_defaults_target_kaggle_t4x2(monkeypatch):
    for name in [
        "QWEN3VL_MODEL_PATH",
        "QWEN3VL_PORT",
        "ENABLE_CLOUDFLARE_TUNNEL",
        "QWEN3VL_API_KEY",
    ]:
        monkeypatch.delenv(name, raising=False)

    settings = Settings.from_env()

    assert settings.port == 8000
    assert settings.enable_cloudflare_tunnel is False
    assert settings.api_key is None
    assert settings.max_upload_bytes == 10 * 1024 * 1024
    assert settings.max_image_dimension == 4096
    assert settings.max_prompt_chars == 16_384
    assert settings.max_schema_bytes == 32 * 1024
    assert settings.default_max_new_tokens == 512
    assert settings.max_new_tokens_limit == 2048
    assert settings.model_path == Path(
        "/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1"
    )


def test_tunnel_mode_fails_closed_without_api_key(monkeypatch):
    monkeypatch.setenv("ENABLE_CLOUDFLARE_TUNNEL", "true")
    monkeypatch.delenv("QWEN3VL_API_KEY", raising=False)

    with pytest.raises(ValueError, match="QWEN3VL_API_KEY"):
        Settings.from_env()


def test_tunnel_mode_accepts_nonempty_api_key(monkeypatch):
    monkeypatch.setenv("ENABLE_CLOUDFLARE_TUNNEL", "1")
    monkeypatch.setenv("QWEN3VL_API_KEY", "test-secret")

    settings = Settings.from_env()

    assert settings.enable_cloudflare_tunnel is True
    assert settings.api_key == "test-secret"


def test_invalid_boolean_is_rejected(monkeypatch):
    monkeypatch.setenv("ENABLE_CLOUDFLARE_TUNNEL", "sometimes")

    with pytest.raises(ValueError, match="boolean"):
        Settings.from_env()
