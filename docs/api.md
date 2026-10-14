# REST API

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](api.vi.md)


Default base URL: `http://127.0.0.1:8000`.

## `GET /health`

Returns readiness only after model initialization completes.

```bash
curl http://127.0.0.1:8000/health
```

## `GET /v1/model`

Reports model/runtime identity including dtype, attention mode, GPU names, device map and offload flags. It never exposes secrets.

```bash
curl http://127.0.0.1:8000/v1/model
```

## `POST /v1/generate`

```bash
curl -X POST http://127.0.0.1:8000/v1/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Explain OCR in three concise sentences.","max_new_tokens":256,"temperature":0}'
```

## `POST /v1/vision`

Multipart upload only. Supported initial formats: JPEG, PNG and WEBP.

```bash
curl -X POST http://127.0.0.1:8000/v1/vision \
  -F 'image=@examples/vision/vision-synthetic-office-rich.png;type=image/png' \
  -F 'prompt=Describe the scene and important spatial relationships.' \
  -F 'max_new_tokens=256' \
  -F 'temperature=0'
```

## `POST /v1/extract`

The `schema` form field uses the repository's compact schema DSL. Every object field is required and extra model-generated fields are rejected during validation.

```bash
curl -X POST http://127.0.0.1:8000/v1/extract \
  -F 'image=@examples/invoices/invoice-01-northstar.png;type=image/png' \
  -F 'schema={"invoice_number":"string","date":"string","total":"number"}' \
  -F 'max_new_tokens=256'
```

Supported primitives are `string`, `number`, `integer`, and `boolean`. Arrays are written with one item schema, for example `[{"name":"string","quantity":"number"}]`.

A structured response is successful only after both JSON parsing and normalized-schema validation pass.

## `GET /v1/metrics`

Returns completed tracked-request counts, endpoint counts, median/p95 latency and CUDA memory snapshots. The metrics request itself is intentionally excluded from its snapshot so totals remain internally consistent.

## Limits

Default implementation limits:

- upload: 10 MiB;
- image dimension: 4096 px on either axis;
- prompt: 16,384 characters;
- compact schema: 32 KiB;
- default `max_new_tokens`: 512;
- hard `max_new_tokens`: 2048;
- active inference concurrency: one request.

These are implementation guardrails, not claims that every boundary has been stress-qualified.

## Public tunnel authentication

When `ENABLE_CLOUDFLARE_TUNNEL=True`, public-host requests require:

```text
Authorization: Bearer <QWEN3VL_API_KEY>
```

Localhost remains usable without authentication. Tunnel startup fails closed if the key is absent.
