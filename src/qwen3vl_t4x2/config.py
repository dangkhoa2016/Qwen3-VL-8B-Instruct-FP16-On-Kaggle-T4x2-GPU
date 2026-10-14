from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


def _parse_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


@dataclass(frozen=True, slots=True)
class Settings:
    model_path: Path
    port: int
    enable_cloudflare_tunnel: bool
    api_key: str | None
    max_upload_bytes: int
    max_image_dimension: int
    max_prompt_chars: int
    max_schema_bytes: int
    default_max_new_tokens: int
    max_new_tokens_limit: int

    @classmethod
    def from_env(cls) -> "Settings":
        model_path = Path(
            os.getenv(
                "QWEN3VL_MODEL_PATH",
                "/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1",
            )
        )
        port = int(os.getenv("QWEN3VL_PORT", "8000"))
        enable_tunnel = _parse_bool(
            os.getenv("ENABLE_CLOUDFLARE_TUNNEL"), default=False
        )
        api_key = os.getenv("QWEN3VL_API_KEY") or None
        if enable_tunnel and not api_key:
            raise ValueError(
                "QWEN3VL_API_KEY is required when ENABLE_CLOUDFLARE_TUNNEL=true"
            )

        return cls(
            model_path=model_path,
            port=port,
            enable_cloudflare_tunnel=enable_tunnel,
            api_key=api_key,
            max_upload_bytes=int(os.getenv("QWEN3VL_MAX_UPLOAD_BYTES", str(10 * 1024 * 1024))),
            max_image_dimension=int(os.getenv("QWEN3VL_MAX_IMAGE_DIMENSION", "4096")),
            max_prompt_chars=int(os.getenv("QWEN3VL_MAX_PROMPT_CHARS", "16384")),
            max_schema_bytes=int(os.getenv("QWEN3VL_MAX_SCHEMA_BYTES", str(32 * 1024))),
            default_max_new_tokens=int(os.getenv("QWEN3VL_DEFAULT_MAX_NEW_TOKENS", "512")),
            max_new_tokens_limit=int(os.getenv("QWEN3VL_MAX_NEW_TOKENS_LIMIT", "2048")),
        )
