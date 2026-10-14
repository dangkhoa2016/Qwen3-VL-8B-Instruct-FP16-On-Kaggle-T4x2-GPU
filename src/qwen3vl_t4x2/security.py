from __future__ import annotations

import hmac

from .config import Settings


def requires_public_auth(host_header: str | None, settings: Settings) -> bool:
    if not settings.enable_cloudflare_tunnel:
        return False
    host = (host_header or "").split(":", 1)[0].strip().lower()
    return host not in {"127.0.0.1", "localhost", "::1"}


def verify_bearer_token(authorization: str | None, settings: Settings) -> None:
    if not authorization:
        raise PermissionError("AUTH_REQUIRED")
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise PermissionError("AUTH_INVALID")
    supplied = authorization[len(prefix):]
    expected = settings.api_key or ""
    if not expected or not hmac.compare_digest(supplied, expected):
        raise PermissionError("AUTH_INVALID")
