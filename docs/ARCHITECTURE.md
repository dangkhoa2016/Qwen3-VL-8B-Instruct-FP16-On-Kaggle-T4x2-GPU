# Architecture

## Purpose

This repository is the production-style showcase for Qwen3-VL-8B-Instruct FP16 on Kaggle Tesla T4 x2. The already-published acceptance notebook remains the baseline qualification authority; this repository focuses on reusable REST serving and deep multimodal demonstrations.

## Runtime topology

```text
Kaggle production-showcase notebook
        |
        | starts one subprocess
        v
FastAPI + Uvicorn on 127.0.0.1:8000
        |
        | loads exactly once
        v
Qwen3-VL-8B-Instruct
FP16 + SDPA + balanced device map
Tesla T4 GPU0 + Tesla T4 GPU1
        |
        +--> internal notebook HTTP client
        +--> optional authenticated Cloudflare Quick Tunnel
```

## Runtime invariants

The loader fails instead of silently degrading if the baseline cannot be honored:

- exactly two CUDA GPUs and both must be Tesla T4;
- `torch.float16` floating weights only;
- SDPA attention;
- `device_map="balanced"` with `12GiB` maximum placement budget per GPU;
- weights must appear on GPU 0 and GPU 1;
- CPU weight offload is forbidden;
- disk weight offload is forbidden;
- the model is a process singleton and is not reloaded per request.

## Service boundaries

The API exposes specialized routes rather than an OpenAI-compatible façade:

- `GET /health`
- `GET /v1/model`
- `POST /v1/generate`
- `POST /v1/vision`
- `POST /v1/extract`
- `GET /v1/metrics`

Image-bearing endpoints accept multipart uploads only. Remote URL fetching and base64 payloads are intentionally unsupported.

## Concurrency

Inference is serialized with one global async lock. Kaggle T4 memory is treated as the limiting resource; reproducibility and stability take priority over throughput.

## Evidence boundary

HTTP/runtime success and semantic quality are separate. Free-form vision responses remain manual review. Structured extraction can be auto-evaluated only after JSON parsing, schema validation and expected-field comparison.
