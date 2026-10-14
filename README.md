# Qwen3-VL-8B-Instruct FP16 on Kaggle T4×2 GPU

<p align="center">
  <a href="https://github.com/dangkhoa2016/Qwen3-VL-8B-Instruct-FP16-On-Kaggle-T4x2-GPU/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/dangkhoa2016/Qwen3-VL-8B-Instruct-FP16-On-Kaggle-T4x2-GPU/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="LICENSE"><img alt="Source License: MIT" src="https://img.shields.io/badge/Source%20License-MIT-yellow.svg"></a>
  <a href="MODEL_LICENSE.md"><img alt="Model License: Apache 2.0" src="https://img.shields.io/badge/Model%20License-Apache%202.0-blue.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
  <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-FP16-EE4C2C?logo=pytorch&logoColor=white">
  <img alt="GPU" src="https://img.shields.io/badge/GPU-Tesla%20T4%20%C3%972-76B900?logo=nvidia&logoColor=white">
  <img alt="Kaggle" src="https://img.shields.io/badge/Kaggle-Production%20Showcase-20BEFF?logo=kaggle&logoColor=white">
  <a href="https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct"><img alt="Model" src="https://img.shields.io/badge/Model-Qwen3--VL--8B--Instruct-6C63FF"></a>
  <img alt="API" src="https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white">
  <img alt="Quantization" src="https://img.shields.io/badge/Quantization-None-0A7E07">
</p>

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

Run **Qwen3-VL-8B-Instruct in native FP16 on two Kaggle Tesla T4 GPUs** and expose it as a reusable multimodal REST service. The project combines strict runtime validation, FastAPI endpoints, schema-driven extraction, controlled multimodal test assets, reproducible evidence, and a reviewer-friendly Kaggle production showcase.

This repository is designed for people who want more than a one-cell inference demo: it shows how to load the model once, verify that it is really split across two T4 GPUs without CPU/disk weight offload, serve text and vision requests through HTTP, exercise structured extraction, inspect latency and GPU memory, and reproduce the workflow on Kaggle.

## What this project provides

- **Native FP16 Qwen3-VL-8B-Instruct** with no GGUF and no quantization.
- **Strict Tesla T4 ×2 runtime checks** with `device_map="balanced"` and a `12 GiB` placement budget per GPU.
- **No CPU or disk weight offload**; startup fails instead of silently degrading the configuration.
- **FastAPI REST service** with text generation, vision understanding, structured extraction, runtime identity, health, and metrics endpoints.
- **Multipart image upload** for JPEG, PNG, and WEBP; no server-side `image_url` fetching and no base64 image payloads.
- **Generic schema-driven JSON extraction** with parse and schema validation.
- **19 canonical multimodal showcase cases** covering seven capability groups.
- **Vietnamese and multilingual examples** in addition to English cases.
- **12-request service stability qualification** on one continuously loaded server instance.
- **Optional authenticated Cloudflare Quick Tunnel**, disabled by default.
- **Bilingual English/Vietnamese documentation**, reproducibility checks, license notes, and repository governance.

## What you can test

| Capability | Examples in this repository |
|---|---|
| General visual understanding | office and market scenes, object/scene description |
| Spatial & relationship reasoning | parking layout, café object relationships |
| OCR & document understanding | notices, warehouse summaries, invoice/receipt understanding |
| Structured JSON extraction | invoice, receipt, business card, service form, Vietnamese delivery note |
| Tables & visual data reasoning | quarterly sales and delivery-performance tables |
| Charts & numerical reasoning | support-ticket bars and satisfaction lines |
| Vietnamese & multilingual | Vietnamese documents, mixed EN/VI workshop content and cross-language questions |

## Runtime architecture

```text
Kaggle Notebook
    |
    | starts one local service process
    v
FastAPI + Uvicorn on 127.0.0.1:8000
    |
    | loads once
    v
Qwen/Qwen3-VL-8B-Instruct
FP16 + SDPA + balanced device map
    |
    +--> Tesla T4 GPU 0
    +--> Tesla T4 GPU 1
    |
    +--> notebook REST client
    +--> optional authenticated Cloudflare Quick Tunnel
```

The model is **sharded across two GPUs**. This is not pooled VRAM and it is not data parallelism. The runtime deliberately favors reproducibility and memory safety over concurrent throughput, so only one inference request is active at a time.

## Runtime configuration

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

The loader verifies the expected two-T4 topology and fails closed if the required placement cannot be honored.

## Run it on Kaggle

Kaggle Notebooks are hosted Jupyter notebooks. Kaggle provides the Python environment, temporary storage, and GPU accelerator, so you do not need a local dual-GPU workstation for this project.

### 1. Create a Kaggle account

Sign in at [kaggle.com](https://www.kaggle.com/). GPU access is subject to Kaggle account eligibility and quota.

### 2. Open or import the notebook

Use either route:

**Route A — start from the Kaggle production showcase**

Open:

[Qwen3-VL-8B FP16 T4x2 Production Showcase](https://www.kaggle.com/code/dangkhoa2016/qwen3-vl-8b-fp16-t4x2-production-showcase)

When the notebook is public, use Kaggle's **Copy & Edit** flow to create an editable copy in your own account.

**Route B — import the repository notebook**

1. Download or clone this repository.
2. Locate `notebooks/kaggle-production-showcase.ipynb`.
3. In Kaggle choose **Create → New Notebook**.
4. In the notebook editor use **File → Import Notebook** and select the `.ipynb` file.

Kaggle UI labels can evolve; the important result is that `kaggle-production-showcase.ipynb` becomes the notebook source in your own Kaggle session.

### 3. Select the correct accelerator

In the notebook editor open **Settings → Accelerator** and choose **GPU T4 ×2**.

This project intentionally requires two NVIDIA Tesla T4 devices. A CPU-only session, a single T4, or a different topology will fail the runtime identity gate rather than silently switching to another execution policy.

### 4. Enable Internet when cloning the repository

The notebook bootstrap can clone the repository when the source is not already present. If you are using that path, enable **Internet** in the Kaggle notebook settings.

If repository source is already available inside the notebook environment, Internet is not required for model inference itself.

### 5. Attach the Kaggle model

From the notebook editor:

1. Open the **Input** pane.
2. Choose **Add Input**.
3. Search for `dangkhoa2016/qwen-qwen3-vl-8b-instruct`.
4. Add the `Transformers / default / 1` model variation.

The expected model path is:

```text
/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1
```

The notebook uses the attached Kaggle model and does **not** silently download a second full checkpoint from Hugging Face.

### 6. Keep Cloudflare disabled for the first run

The normal path is local-only:

```text
ENABLE_CLOUDFLARE_TUNNEL=False
```

You do not need a public tunnel to execute or validate the notebook.

### 7. Start from a clean session and run everything

For the most reproducible run:

1. restart the Kaggle session if it has already loaded other large models;
2. confirm **GPU T4 ×2** is still selected;
3. confirm the model is attached;
4. use **Run All**.

The notebook will:

1. verify repository/source identity;
2. verify the two-T4 environment;
3. verify controlled showcase assets;
4. start the FastAPI service on localhost;
5. wait for `/health` readiness;
6. inspect `/v1/model` to prove FP16 dual-T4 placement and no CPU/disk offload;
7. run REST examples;
8. execute the 19 canonical showcase cases exactly once;
9. render the stored results by capability instead of re-running inference;
10. perform the 12-request service stability check;
11. display metrics, GPU memory snapshots, a results dashboard, and the final scorecard.

### 8. Read the final scorecard

A successful run should show, among other fields:

- the resolved repository commit;
- model identity;
- `torch.float16` dtype;
- both Tesla T4 GPU names;
- no CPU/disk weight offload;
- canonical showcase runtime status;
- structured JSON parse/schema rates;
- structured semantic checks;
- service stability status;
- latency summary;
- Cloudflare status.

Do not interpret HTTP 200 as automatic semantic correctness. Free-form answers remain reviewable model output; only the defined structured cases receive automatic expected-field evaluation.

### 9. Save your Kaggle run

After a successful execution, use Kaggle's **Save Version** workflow if you want a persistent notebook version with outputs. Review outputs and secrets before making any copy public.

For a longer walkthrough and troubleshooting notes, see [docs/kaggle.md](docs/kaggle.md).

## REST API

Default base URL:

```text
http://127.0.0.1:8000
```

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness/readiness after model initialization |
| `GET` | `/v1/model` | Model, dtype, attention, GPU placement and offload identity |
| `POST` | `/v1/generate` | Text-only generation |
| `POST` | `/v1/vision` | Image + prompt inference |
| `POST` | `/v1/extract` | Generic schema-driven extraction |
| `GET` | `/v1/metrics` | Request counts, latency and CUDA memory snapshots |

### Text generation

```bash
curl -X POST http://127.0.0.1:8000/v1/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Explain OCR in three concise sentences.","max_new_tokens":256,"temperature":0}'
```

### Vision

```bash
curl -X POST http://127.0.0.1:8000/v1/vision \
  -F 'image=@examples/realistic/cozy_daylight_workspace_with_city_views.jpg;type=image/jpeg' \
  -F 'prompt=Describe the scene and important spatial relationships.' \
  -F 'max_new_tokens=256' \
  -F 'temperature=0'
```

### Structured extraction

```bash
curl -X POST http://127.0.0.1:8000/v1/extract \
  -F 'image=@examples/realistic/northstar_office_supply_invoice.jpg;type=image/jpeg' \
  -F 'schema={"invoice_number":"string","date":"string","total":"number"}' \
  -F 'max_new_tokens=256'
```

The compact schema DSL supports `string`, `number`, `integer`, `boolean`, nested objects, and arrays with one item schema. Every object field is required and extra model-generated fields are rejected during validation.

Default implementation guardrails include a 10 MiB upload limit, 4096-pixel maximum image dimension, 16,384-character prompt limit, 32 KiB schema limit, and `2048` hard `max_new_tokens` ceiling. See [docs/api.md](docs/api.md) for the complete contract.

## Production showcase

The notebook executes **19 canonical cases exactly once** and then reuses stored results for galleries and the dashboard. The catalog spans seven capability groups:

1. **General Visual Understanding**
2. **Spatial & Relationship Reasoning**
3. **OCR & Document Understanding**
4. **Structured JSON Extraction**
5. **Tables & Visual Data Reasoning**
6. **Charts & Numerical Reasoning**
7. **Vietnamese & Multilingual**

Five structured cases receive automatic semantic checks. Free-form vision/document answers are intentionally kept separate from runtime success and require human review for quality judgments.

## Verified development evidence

The following measurements were captured during verified T4×2 development runs. They are **development-session evidence**, not a substitute for the reviewed official evidence set referenced by `benchmarks/official/` and published through the exact Kaggle execution plus matching GitHub Release assets.

```text
SHOWCASE_CASES_TOTAL=19
SHOWCASE_RUNTIME_PASS=19
SHOWCASE_RUNTIME_FAIL=0
STRUCTURED_CASES_TOTAL=5
STRUCTURED_JSON_PARSE_RATE=100%
STRUCTURED_SCHEMA_VALID_RATE=100%
STRUCTURED_EXPECTED_FIELD_CHECKS=5/5 PASS
FREE_FORM_MANUAL_REVIEW=14/14
```

A separate 12-request stability run on one continuously loaded server instance recorded:

```text
/v1/generate: 6
/v1/vision: 3
/v1/extract: 3
REQUESTS_PASS=12/12
MODEL_IDENTITY_STABLE=true
GPU0_ALLOCATED_DELTA=0 bytes
GPU1_ALLOCATED_DELTA=0 bytes
SERVICE_STABILITY_GATE=PASS
```

The repository deliberately separates three concepts:

- **runtime success** — request/service execution completed;
- **structured semantic checks** — defined fields match controlled expectations after strict normalization;
- **free-form quality** — requires human review and is not auto-PASSed because an HTTP request succeeded.

See [docs/benchmarks.md](docs/benchmarks.md) and [docs/benchmark-methodology.md](docs/benchmark-methodology.md) for methodology and caveats.

## Baseline acceptance vs. production showcase

These two artifacts serve different purposes:

| Artifact | Purpose |
|---|---|
| [Qwen3-VL-8B FP16 Kaggle T4×2 Production Acceptance](https://www.kaggle.com/code/dangkhoa2016/qwen3-vl-8b-fp16-kaggle-t4x2-production-acceptance) | Baseline qualification for native FP16 viability, T4×2 placement, context/stability/OOM characterization and acceptance evidence |
| This repository + `notebooks/kaggle-production-showcase.ipynb` | Reusable REST serving, deep multimodal cases, structured extraction, service metrics/stability and presentation-oriented evidence |

The production showcase complements the baseline acceptance notebook; it does not redefine or replace the baseline acceptance criteria.

## Optional Cloudflare Quick Tunnel

Localhost is the recommended default. To expose the API temporarily:

```text
ENABLE_CLOUDFLARE_TUNNEL=True
QWEN3VL_API_KEY=<secret>
```

Tunnel startup refuses to expose the service if the API key is absent. Requests arriving through the public host require:

```text
Authorization: Bearer <QWEN3VL_API_KEY>
```

Localhost remains unauthenticated. Never print, store in notebook output, or commit the API key. See [docs/security.md](docs/security.md).

## Repository structure

```text
.github/                  CI, Dependabot, issue/PR templates and community health files
benchmarks/official/      reviewed public benchmark artifacts only
docs/                     architecture, API, Kaggle, benchmark, security and engineering guides
evidence/                 evidence policy and provenance boundary
examples/                 controlled multimodal assets
ground_truth/             canonical case catalog, schemas and expected facts
notebooks/                Kaggle production-showcase notebook
scripts/                  server, showcase, stability and verification helpers
src/qwen3vl_t4x2/         runtime, generation, API, metrics, security and evidence code
tests/                    unit, mocked and API-contract tests
```

## Reproduce the repository checks

```bash
pytest -q
python -m compileall -q src scripts
python scripts/verify_asset_pack.py .
python scripts/verify_notebook.py notebooks/kaggle-production-showcase.ipynb
python scripts/verify_no_secrets.py .
python scripts/verify_repository.py
```

The CI workflow intentionally uses unit, mocked, API-contract, static and repository checks. It does **not** claim that CI output is real GPU inference evidence.

## Troubleshooting

| Symptom | What to check |
|---|---|
| Model startup fails | model attachment, expected model path, two visible Tesla T4 GPUs, available VRAM |
| Runtime reports one GPU | confirm **Settings → Accelerator → GPU T4 ×2**, then restart the session |
| CPU/disk appears in device map | treat the run as invalid; this project intentionally rejects weight offload |
| Model path is missing | re-add `dangkhoa2016/qwen-qwen3-vl-8b-instruct` from the Input pane |
| Repository clone fails | enable Internet for the clone path or provide repository source another way |
| `/v1/vision` rejects an image | use JPEG/PNG/WEBP and stay within upload/dimension limits |
| `/v1/extract` rejects output | inspect raw model output; JSON/schema validation intentionally fails closed |
| Tunnel returns `401` | set `QWEN3VL_API_KEY` and send the Bearer token |
| Session behaves inconsistently after experiments | restart the Kaggle session and run the notebook from the top |

More cases are documented in [docs/troubleshooting.md](docs/troubleshooting.md).

## Documentation

- [Documentation index](docs/index.md) / [Mục lục tài liệu](docs/index.vi.md)
- [Architecture](docs/architecture.md) / [Kiến trúc](docs/architecture.vi.md)
- [REST API](docs/api.md) / [REST API — VI](docs/api.vi.md)
- [Kaggle execution guide](docs/kaggle.md) / [Hướng dẫn Kaggle](docs/kaggle.vi.md)
- [Benchmarks](docs/benchmarks.md) / [Benchmark — VI](docs/benchmarks.vi.md)
- [Benchmark methodology](docs/benchmark-methodology.md) / [Phương pháp benchmark](docs/benchmark-methodology.vi.md)
- [Reproducibility](docs/reproducibility.md) / [Tái lập](docs/reproducibility.vi.md)
- [Troubleshooting](docs/troubleshooting.md) / [Xử lý sự cố](docs/troubleshooting.vi.md)
- [Security](docs/security.md) / [Bảo mật](docs/security.vi.md)
- [Limitations](docs/limitations.md) / [Giới hạn](docs/limitations.vi.md)
- [Contributing](CONTRIBUTING.md) / [Đóng góp](CONTRIBUTING.vi.md)
- [Changelog](CHANGELOG.md) / [Changelog — VI](CHANGELOG.vi.md)

## License and attribution

Original source code and documentation in this repository are licensed under the [MIT License](LICENSE), copyright **Đăng Khoa**.

The Qwen3-VL model weights are **not redistributed by this repository**. The model is attached separately through Kaggle. Upstream `Qwen/Qwen3-VL-8B-Instruct` is distributed under Apache-2.0; see [MODEL_LICENSE.md](MODEL_LICENSE.md), [LICENSE-NOTES.md](LICENSE-NOTES.md), and [THIRD_PARTY_LICENSES/QWEN3-VL-APACHE-2.0.txt](THIRD_PARTY_LICENSES/QWEN3-VL-APACHE-2.0.txt).

Showcase asset provenance and hashes are documented in [LICENSE-SOURCES.md](LICENSE-SOURCES.md) and [ASSET_MANIFEST.json](ASSET_MANIFEST.json). The controlled release showcase does not require third-party web photographs.
