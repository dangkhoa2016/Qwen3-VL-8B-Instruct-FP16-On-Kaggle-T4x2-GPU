# Security Policy

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](SECURITY.vi.md)

## Runtime posture

The default FastAPI service binds to localhost. Cloudflare Quick Tunnel is optional and disabled by default. When public exposure is enabled, `QWEN3VL_API_KEY` is mandatory and public-host requests require Bearer authentication.

The implementation fails closed when tunnel mode is enabled without a key. Secrets must not be printed or committed.

## Reporting

Do not publish credentials, private data or exploitable details in a public issue. Report sensitive issues privately to the repository owner using the contact channel on the GitHub profile. Include the affected commit, reproduction and impact.

See [docs/security.md](docs/security.md) for the detailed threat model.
