# Qwen3-VL T4x2 Production Showcase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable FastAPI service and Kaggle production-showcase harness for Qwen3-VL-8B-Instruct in native FP16 on T4x2, backed by deterministic multimodal evidence assets.

**Architecture:** The Kaggle notebook launches one Python FastAPI/Uvicorn process. The process loads the attached Qwen3-VL model exactly once, exposes specialized text/vision/extraction endpoints, serializes inference with one global lock, records lightweight metrics, and optionally supports authenticated Cloudflare exposure while localhost remains usable without authentication.

**Tech Stack:** Python 3.13, PyTorch, Transformers, Accelerate, FastAPI, Uvicorn, Pillow, jsonschema, HTTPX/requests, pytest.

**Spec:** User-provided `Qwen3-VL-8B-Instruct-FP16-On-Kaggle-T4x2-GPU-DESIGN-SPEC-v0.1.md` (conversation attachment; not copied into this Kaggle workspace).

## Global Constraints

- Model: `Qwen/Qwen3-VL-8B-Instruct` from Kaggle attachment `dangkhoa2016/qwen-qwen3-vl-8b-instruct`.
- Dtype: `torch.float16`; quantization is forbidden.
- Baseline: two Tesla T4 GPUs, balanced weight placement, no CPU weight offload, no disk weight offload, batch size 1.
- Server: FastAPI + Uvicorn, specialized endpoints `/health`, `/v1/model`, `/v1/generate`, `/v1/vision`, `/v1/extract`, `/v1/metrics`.
- Image input: multipart file upload only; JPEG/PNG/WEBP; no `image_url`, no base64, no remote URL fetch.
- Structured extraction: schema-driven; success only after JSON parsing and schema validation.
- Concurrency: one active inference request at a time.
- Cloudflare: `ENABLE_CLOUDFLARE_TUNNEL=False` by default; public tunnel must fail closed without `QWEN3VL_API_KEY`.
- Evidence: runtime HTTP success and semantic/schema validation are separate results.

## Review Focus

- Corrupt/unsupported image uploads must return stable JSON errors and never reach inference.
- Invalid extraction schemas must fail before inference.
- Public-tunnel mode with missing API key must fail closed.
- Runtime metadata must prove FP16/T4x2 placement and reject CPU/disk offload.
- Concurrent requests must be serialized to avoid avoidable T4 OOM.

---

### Task 1: Configuration and project skeleton

**Files:** Create `pyproject.toml`, `src/qwen3vl_t4x2/config.py`, `tests/test_config.py`.

**Interfaces:** `Settings.from_env() -> Settings`; produces model path, port, limits, tunnel/auth policy and generation defaults.

- [ ] Write config tests first and verify RED.
- [ ] Implement immutable settings + environment parsing.
- [ ] Run focused tests and full `pytest` GREEN.
- [ ] Commit.

### Task 2: Extraction schema validation

**Files:** Create `src/qwen3vl_t4x2/schemas.py`, `tests/test_schema_validation.py`.

**Interfaces:** `normalize_schema(spec: object) -> dict`; `validate_extracted(value: object, normalized: dict) -> None`; `build_extraction_instruction(spec: object) -> str`.

- [ ] Write schema tests first and verify RED.
- [ ] Implement the supported compact schema DSL (`string`, `number`, `integer`, `boolean`, arrays, nested objects).
- [ ] Verify invalid types/oversized schema/nested extraction cases.
- [ ] Commit.

### Task 3: Runtime identity and strict model loader

**Files:** Create `src/qwen3vl_t4x2/runtime.py`, `tests/test_runtime.py`.

**Interfaces:** `RuntimeInfo`; `ModelRuntime.load(settings) -> ModelRuntime`; `audit_device_map(model) -> dict`; `runtime_info() -> RuntimeInfo`.

- [ ] Test audit logic with synthetic device maps first and verify RED.
- [ ] Implement FP16/no-offload/two-GPU audit and lazy single-load lifecycle.
- [ ] Smoke-load the real Kaggle model and record exact observed device map without changing strategy silently.
- [ ] Commit.

### Task 4: Generation pipeline

**Files:** Create `src/qwen3vl_t4x2/generation.py`, `tests/test_generation.py`.

**Interfaces:** text generation, image+prompt generation, extraction generation; each returns output + token/latency metadata.

- [ ] Write tests using a fake runtime and verify RED.
- [ ] Implement Qwen3-VL processor chat-template path, deterministic generation defaults, image decoding/validation, token accounting.
- [ ] Real text and vision smoke tests on T4x2.
- [ ] Commit.

### Task 5: Metrics and specialized REST API

**Files:** Create `src/qwen3vl_t4x2/metrics.py`, `src/qwen3vl_t4x2/api.py`, `tests/test_api_contract.py`.

**Interfaces:** FastAPI app factory `create_app(settings, runtime=None)` and all six public endpoints.

- [ ] Write mocked API-contract tests first and verify RED.
- [ ] Implement readiness lifecycle, one global inference lock, consistent JSON errors, multipart endpoints and metrics.
- [ ] Run contract suite and real local server smoke tests.
- [ ] Commit.

### Task 6: Tunnel security and launch scripts

**Files:** Create `src/qwen3vl_t4x2/security.py`, `tests/test_security.py`, `scripts/start_server.py`, `scripts/start_cloudflare_tunnel.sh`, `scripts/run_smoke.py`.

**Interfaces:** localhost bypass policy; public Bearer-token verifier; startup refuses tunnel mode without key.

- [ ] Write security tests first and verify RED.
- [ ] Implement fail-closed policy and launch helpers.
- [ ] Verify localhost flow without key and configuration failure when tunnel enabled without key.
- [ ] Commit.

### Task 7: Asset/evidence harness and production-showcase notebook

**Files:** Modify `ground_truth/cases.json`; create `scripts/run_showcase.py`, `scripts/verify_evidence.py`, `notebooks/kaggle-production-showcase.ipynb`.

**Interfaces:** JSONL case evidence, JSON summary, separate runtime/semantic verdicts.

- [ ] Add tests for evidence aggregation before implementation.
- [ ] Integrate current synthetic assets and later realistic assets without third-party fetch dependency for the default release set.
- [ ] Build notebook orchestration: attach instructions, runtime snapshot, server launch, `/health`, `/v1/model`, showcase suites, sequential service test, final summary.
- [ ] Execute representative cases and verify generated evidence.
- [ ] Commit.

## Implementation Status — 2026-10-14

Completed and locally verified on Kaggle T4 x2:

- [x] repository/bootstrap and deterministic asset pack;
- [x] strict FP16/SDPA/balanced T4 x2 runtime loader with no-offload audit;
- [x] text, multipart vision and generic schema-driven extraction pipelines;
- [x] six specialized REST endpoints with serialized inference;
- [x] localhost/public-host authentication boundary and tunnel fail-closed policy;
- [x] metrics with internally consistent snapshots;
- [x] machine-readable evidence runner and independent verifier;
- [x] 19-case development showcase: 19/19 runtime PASS, 5/5 structured expected-field PASS after narrow typography normalization;
- [x] 12-request sequential service stability: 12/12 PASS, zero allocated-memory growth on both GPUs;
- [x] production-showcase notebook with one inference campaign and evidence rendering by capability;
- [x] EN/VI architecture/API/Kaggle/security/benchmark documentation and GitHub CI/governance skeleton.

Remaining before public v1.0.0:

- [ ] promote the selected photorealistic AI-generated assets into the repository/Kaggle workspace and update the manifest/cases;
- [ ] execute the final production-showcase notebook on the official Kaggle account and review every free-form semantic result;
- [ ] promote reviewed official evidence to `benchmarks/official/`;
- [x] verify the authoritative upstream Qwen3-VL model license and finalize attribution wording (Apache-2.0 upstream; verified 2026-10-14);
- [ ] push the local commit history to GitHub, observe public CI PASS, then finalize release metadata/tag `v1.0.0`.


### Task 8: Documentation/governance and final verification

**Files:** Create `.github/`, EN/VI docs, `LICENSE`, `CITATION.cff`, `CHANGELOG*`, `README*`, lock file.

- [ ] Generate measured benchmark docs only from real evidence.
- [ ] Run full tests/static checks/no-secret scan.
- [ ] Review commit history; keep README EN/VI finalization last.
- [ ] Do not push/tag/release until explicit user authorization and GitHub credential is available.
