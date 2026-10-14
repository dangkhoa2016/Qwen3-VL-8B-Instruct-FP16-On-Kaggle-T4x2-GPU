# Qwen3-VL-8B-Instruct FP16 on Kaggle T4×2 GPU

[![CI](https://github.com/dangkhoa2016/Qwen3-VL-8B-Instruct-FP16-On-Kaggle-T4x2-GPU/actions/workflows/ci.yml/badge.svg)](https://github.com/dangkhoa2016/Qwen3-VL-8B-Instruct-FP16-On-Kaggle-T4x2-GPU/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](pyproject.toml)
[![Kaggle GPU](https://img.shields.io/badge/Kaggle-Tesla%20T4%20%C3%972-20BEFF.svg)](docs/KAGGLE.md)

A production-style reference implementation for running **Qwen3-VL-8B-Instruct in native FP16 on Kaggle Tesla T4 ×2**, with a reusable FastAPI REST service and a deep multimodal production-showcase notebook.

> **Status:** implementation, self-contained photorealistic assets and local Kaggle development evidence are complete. Final public notebook execution, GitHub CI publication, reviewed official evidence and `v1.0.0` remain release gates.

**Tiếng Việt:** [README.vi.md](README.vi.md)

## Project positioning

This repository does not replace the baseline acceptance notebook.

| Artifact | Role |
|---|---|
| [Qwen3-VL-8B FP16 Kaggle T4×2 Production Acceptance](https://www.kaggle.com/code/dangkhoa2016/qwen3-vl-8b-fp16-kaggle-t4x2-production-acceptance) | Baseline qualification authority: FP16/T4×2 placement, stability/context/OOM and acceptance evidence |
| This repository + `notebooks/kaggle-production-showcase.ipynb` | Reusable REST service, deep multimodal examples, structured extraction, metrics and reviewer-facing evidence |

The practical goal is simple: **show how Qwen3-VL-8B-Instruct FP16 can actually be used on Kaggle T4×2 as a reusable multimodal service.**

## Highlights

- native `torch.float16`; no quantization;
- strict Tesla T4 ×2 placement with `device_map="balanced"`;
- no CPU or disk weight offload;
- FastAPI + Uvicorn, with one model load reused across requests;
- specialized `/health`, `/v1/model`, `/v1/generate`, `/v1/vision`, `/v1/extract`, `/v1/metrics` endpoints;
- multipart image upload only; no server-side URL fetch and no base64 image input;
- generic schema-driven extraction with JSON parse + schema validation;
- one active inference request at a time for reproducibility and memory safety;
- optional Cloudflare Quick Tunnel, disabled by default and fail-closed without an API key;
- machine-readable JSONL/JSON evidence that keeps runtime success separate from semantic quality;
- six AI-generated photorealistic showcase assets with no required third-party web photographs;
- EN/VI documentation and a Kaggle production-showcase notebook.

## Runtime baseline

```text
model: Qwen/Qwen3-VL-8B-Instruct
source: Kaggle Model attachment
precision: torch.float16
attention: SDPA
device_map: balanced
max_memory GPU 0: 12 GiB
max_memory GPU 1: 12 GiB
batch size: 1
CPU weight offload: forbidden
Disk weight offload: forbidden
```

The loader fails instead of silently changing precision, quantizing, offloading weights, or switching device-map strategy.

## REST API

Default base URL: `http://127.0.0.1:8000`.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness/readiness |
| `GET` | `/v1/model` | Runtime identity and placement evidence |
| `POST` | `/v1/generate` | Text-only generation |
| `POST` | `/v1/vision` | Image + prompt inference |
| `POST` | `/v1/extract` | Generic schema-driven extraction |
| `GET` | `/v1/metrics` | Request/latency/GPU memory snapshots |

Vision example:

```bash
curl -X POST http://127.0.0.1:8000/v1/vision \
  -F 'image=@examples/realistic/cozy_daylight_workspace_with_city_views.jpg;type=image/jpeg' \
  -F 'prompt=Describe the scene and important spatial relationships.' \
  -F 'max_new_tokens=256' \
  -F 'temperature=0'
```

Structured extraction example:

```bash
curl -X POST http://127.0.0.1:8000/v1/extract \
  -F 'image=@examples/realistic/northstar_office_supply_invoice.jpg;type=image/jpeg' \
  -F 'schema={"invoice_number":"string","date":"string","total":"number"}' \
  -F 'max_new_tokens=256'
```

See [docs/API.md](docs/API.md) for the complete contract and limits.

## Kaggle quick start

1. Create/open a Kaggle Notebook and select **GPU T4 ×2**.
2. Attach [`dangkhoa2016/qwen-qwen3-vl-8b-instruct`](https://www.kaggle.com/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct).
3. Confirm `/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1` exists.
4. Run `notebooks/kaggle-production-showcase.ipynb`.

The notebook does **not** silently download a second full checkpoint. It verifies hardware/assets, starts the REST server, audits `/v1/model`, runs the multimodal catalog once, renders evidence by capability, runs service stability, and prints the final summary.

See [docs/KAGGLE.md](docs/KAGGLE.md) for details.

## Showcase capability groups

The controlled catalog covers five groups:

1. **General Vision Understanding** — objects, fine details, spatial and multi-object relationships.
2. **OCR + Document Understanding** — notices, operational summaries, invoice/receipt understanding beyond transcription.
3. **Generic Structured Extraction** — invoice, receipt, business card and form schemas.
4. **Tables / Charts / Visual Reasoning** — lookup, comparisons, trends and cross-cell/cross-series reasoning.
5. **Multilingual & Mixed Context** — English/Vietnamese images, prompts and extraction.

Free-form answers are deliberately **not** auto-labeled quality PASS merely because HTTP returned 200. Structured extraction is auto-evaluated only after JSON parse, normalized-schema validation and expected-field comparison.

## Development evidence — 2026-10-14

These are verified **development-session results**, not yet the final public production-showcase benchmark.

```text
SHOWCASE_CASES_TOTAL=19
SHOWCASE_RUNTIME_PASS=19
SHOWCASE_RUNTIME_FAIL=0
STRUCTURED_CASES_TOTAL=5
STRUCTURED_JSON_PARSE_RATE=100%
STRUCTURED_SCHEMA_VALID_RATE=100%
STRUCTURED_EXPECTED_FIELD_CHECKS=5/5 PASS
FREE_FORM_MANUAL_REVIEW=14/14
MEDIAN_CASE_WALL_LATENCY=13,822 ms
```

The expected-field evaluator uses only narrow equivalence normalization: Unicode NFKC, whitespace collapse, and typographic-dash equivalence. It does not relax numeric values or arbitrary content.

A 12-request stability run on one continuously loaded server produced:

```text
6 × /v1/generate
3 × /v1/vision
3 × /v1/extract
REQUESTS_PASS=12/12
MEDIAN_WALL_LATENCY=3,357 ms
MAX_WALL_LATENCY=15,482 ms
MODEL_IDENTITY_STABLE=true
GPU0_ALLOCATED_DELTA=0 bytes
GPU1_ALLOCATED_DELTA=0 bytes
GPU0_RESERVED_DELTA=+4 MiB
GPU1_RESERVED_DELTA=+4 MiB
SERVICE_STABILITY_GATE=PASS
```

See [docs/BENCHMARKS.md](docs/BENCHMARKS.md) for methodology and caveats.

## Evidence model

Session outputs are written to `results/` and intentionally ignored by Git. Evidence becomes a versioned public artifact only after an official Kaggle execution is reviewed and deliberately promoted to `benchmarks/official/`.

This prevents CI/mock output from being confused with actual T4×2 evidence.

## Security and optional Cloudflare tunnel

Normal execution is localhost-only:

```text
ENABLE_CLOUDFLARE_TUNNEL=False
```

Public Quick Tunnel access is opt-in:

```text
ENABLE_CLOUDFLARE_TUNNEL=True
QWEN3VL_API_KEY=<secret>
```

Tunnel startup refuses to proceed if the key is missing. Public-host requests require `Authorization: Bearer <QWEN3VL_API_KEY>`; localhost remains unauthenticated. Never print or commit the key.

See [docs/SECURITY.md](docs/SECURITY.md).

## Repository structure

```text
.github/                  GitHub CI, Dependabot and templates
benchmarks/official/      reviewed public benchmark artifacts only
docs/                     architecture, API, Kaggle, benchmark and security docs
evidence/                 evidence policy
examples/                 deterministic multimodal benchmark assets
ground_truth/             case catalog, schemas and expected facts
notebooks/                Kaggle production-showcase notebook
scripts/                  server, showcase, stability and verification helpers
src/qwen3vl_t4x2/         runtime, generation, API, metrics, security and evidence code
tests/                    mocked/unit/API-contract tests
```

## Verification

```bash
pytest -q
python scripts/verify_asset_pack.py .
python scripts/verify_notebook.py notebooks/kaggle-production-showcase.ipynb
python -m compileall -q src scripts
```

Fresh local release-candidate gates for the self-contained **23-asset / 19-case** catalog: **40 tests PASS**, asset verifier PASS, notebook static verifier PASS (`34` cells, one showcase run), secret scan PASS (`64` text files scanned), and canonical development evidence verifier PASS (`19/19` runtime cases).

CI intentionally uses mocked/API-contract tests and static verification; it does not present CI as real GPU evidence.

## Known limits / remaining release gates

Before public `v1.0.0`:

- the final production-showcase notebook must be executed and reviewed on the official Kaggle account;
- reviewed official evidence must be promoted to `benchmarks/official/`;
- GitHub CI must pass after the local history is pushed.

Out of scope for the initial release: custom web UI, Gradio/Streamlit, OpenAI-compatible API, `image_url`, base64 image input, quantization, vLLM/SGLang, multi-user accounts, persistent database and external production-cloud deployment.

## License and upstream model

Original repository code and documentation are licensed under [MIT](LICENSE).

Qwen3-VL model weights are **not redistributed** here; users attach them separately through Kaggle. Upstream `Qwen/Qwen3-VL-8B-Instruct` is Apache-2.0; the weights are attached separately and are not redistributed by this repository. See [LICENSE-NOTES.md](LICENSE-NOTES.md).

Asset provenance and hashes are documented in [LICENSE-SOURCES.md](LICENSE-SOURCES.md) and [ASSET_MANIFEST.json](ASSET_MANIFEST.json). No third-party web photograph is required by the release showcase.

## Documentation

- [Architecture](docs/ARCHITECTURE.md) / [Kiến trúc](docs/ARCHITECTURE.vi.md)
- [REST API](docs/API.md) / [REST API — VI](docs/API.vi.md)
- [Kaggle guide](docs/KAGGLE.md) / [Kaggle — VI](docs/KAGGLE.vi.md)
- [Benchmarks](docs/BENCHMARKS.md) / [Benchmark — VI](docs/BENCHMARKS.vi.md)
- [Security](docs/SECURITY.md) / [Bảo mật](docs/SECURITY.vi.md)
- [Contributing](CONTRIBUTING.md) / [Đóng góp](CONTRIBUTING.vi.md)
- [Changelog](CHANGELOG.md) / [Changelog — VI](CHANGELOG.vi.md)
