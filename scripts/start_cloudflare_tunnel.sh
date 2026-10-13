#!/usr/bin/env bash
set -euo pipefail

flag="${ENABLE_CLOUDFLARE_TUNNEL:-False}"
case "${flag,,}" in
  1|true|yes|on) ;;
  *) echo "CLOUDFLARE_TUNNEL=DISABLED"; exit 0 ;;
esac

if [[ -z "${QWEN3VL_API_KEY:-}" ]]; then
  echo "ERROR: QWEN3VL_API_KEY is required when ENABLE_CLOUDFLARE_TUNNEL=True" >&2
  exit 2
fi

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "ERROR: cloudflared executable not found" >&2
  exit 3
fi

port="${QWEN3VL_PORT:-8000}"
exec cloudflared tunnel --no-autoupdate --url "http://127.0.0.1:${port}"
