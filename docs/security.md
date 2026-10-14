# Security Model

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](security.vi.md)


This project is a Kaggle demo/reference implementation, not a hardened multi-tenant internet service.

## Defaults

- the server binds to `127.0.0.1`;
- Cloudflare Quick Tunnel is disabled by default;
- localhost does not require an API key;
- enabling the public-tunnel policy without `QWEN3VL_API_KEY` fails closed;
- public-host requests use Bearer-token verification with constant-time comparison;
- secrets are never returned by `/v1/model` or `/v1/metrics`.

## Upload surface

The service accepts only JPEG, PNG and WEBP multipart uploads, with file-size and dimension limits. It does not fetch remote image URLs and does not accept base64 image payloads. Uploaded images are decoded in memory and are not permanently stored by default.

## Request controls

Prompt length, schema bytes and output-token limits are explicit. Inference is serialized with a global lock to reduce avoidable GPU OOM risk.

## Reporting

Do not open a public GitHub issue containing credentials or private data. See root `SECURITY.md` for the reporting policy.
