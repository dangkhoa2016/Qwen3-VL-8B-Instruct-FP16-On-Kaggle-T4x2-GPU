# Qwen3-VL-8B-Instruct FP16 trên Kaggle T4×2 GPU

[![CI](https://github.com/dangkhoa2016/Qwen3-VL-8B-Instruct-FP16-On-Kaggle-T4x2-GPU/actions/workflows/ci.yml/badge.svg)](https://github.com/dangkhoa2016/Qwen3-VL-8B-Instruct-FP16-On-Kaggle-T4x2-GPU/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Kaggle GPU](https://img.shields.io/badge/Kaggle-Tesla%20T4%20%C3%972-20BEFF.svg)](docs/KAGGLE.vi.md)

Repository production-style để chạy **Qwen3-VL-8B-Instruct native FP16 trên Kaggle Tesla T4 ×2**, cung cấp FastAPI REST service tái sử dụng và một notebook production showcase multimodal sâu.

> **Trạng thái:** implementation, bộ photorealistic assets self-contained và local development evidence trên Kaggle đã hoàn thành. Final public notebook execution, public GitHub CI, reviewed official evidence và release `v1.0.0` vẫn là các release gate còn lại.

**English:** [README.md](README.md)

## Vai trò của repository

Repository này không thay thế notebook acceptance đã publish.

| Artifact | Vai trò |
|---|---|
| [Qwen3-VL-8B FP16 Kaggle T4×2 Production Acceptance](https://www.kaggle.com/code/dangkhoa2016/qwen3-vl-8b-fp16-kaggle-t4x2-production-acceptance) | Nguồn chứng cứ baseline: FP16/T4×2 placement, stability/context/OOM và acceptance |
| Repository này + `notebooks/kaggle-production-showcase.ipynb` | REST service, deep multimodal examples, structured extraction, metrics và evidence cho reviewer |

Mục tiêu thực tế: **chứng minh cách dùng Qwen3-VL-8B-Instruct FP16 trên Kaggle T4×2 như một multimodal service tái sử dụng được.**

## Điểm chính

- native `torch.float16`, không quantization;
- strict Tesla T4 ×2 với `device_map="balanced"`;
- không CPU/disk weight offload;
- FastAPI + Uvicorn, model chỉ load một lần;
- endpoint chuyên biệt: `/health`, `/v1/model`, `/v1/generate`, `/v1/vision`, `/v1/extract`, `/v1/metrics`;
- image chỉ qua multipart upload, không URL/base64;
- generic schema-driven extraction với JSON parse + schema validation;
- một inference request active tại một thời điểm;
- Cloudflare Quick Tunnel là tùy chọn, tắt mặc định và fail-closed nếu thiếu API key;
- evidence JSONL/JSON tách runtime success khỏi semantic quality.
- 6 photorealistic assets do AI tạo riêng cho dự án; release không cần ảnh web bên thứ ba.

## Baseline runtime

```text
model: Qwen/Qwen3-VL-8B-Instruct
precision: torch.float16
attention: SDPA
device_map: balanced
max_memory: 12 GiB mỗi GPU
batch size: 1
CPU weight offload: cấm
Disk weight offload: cấm
```

Startup sẽ fail rõ ràng thay vì âm thầm đổi precision, quantize, offload hoặc đổi device-map strategy.

## Kaggle quick start

1. Tạo/mở Kaggle Notebook và chọn **GPU T4 ×2**.
2. Attach [`dangkhoa2016/qwen-qwen3-vl-8b-instruct`](https://www.kaggle.com/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct).
3. Xác nhận path `/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1`.
4. Chạy `notebooks/kaggle-production-showcase.ipynb`.

Notebook không tải thêm full checkpoint thứ hai. Nó kiểm tra hardware/assets, start REST service, audit `/v1/model`, chạy catalog multimodal đúng một lần, hiển thị evidence theo capability, chạy stability gate và in final summary.

Xem [docs/KAGGLE.vi.md](docs/KAGGLE.vi.md).

## 5 nhóm showcase

1. **General Vision Understanding** — object, chi tiết nhỏ, spatial/multi-object relationship.
2. **OCR + Document Understanding** — notice, business document, invoice/receipt understanding.
3. **Generic Structured Extraction** — invoice, receipt, business card, form.
4. **Tables / Charts / Visual Reasoning** — lookup, comparison, trend, cross-cell/cross-series.
5. **Multilingual & Mixed Context** — English/Vietnamese image, prompt và extraction.

Free-form output không auto-PASS chỉ vì HTTP 200. Structured extraction chỉ auto-evaluate sau JSON parse, schema validation và expected-field check.

## Development evidence — 2026-10-14

Đây là số đo development đã verify, **chưa phải final public benchmark**:

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

Service stability trên cùng một model/server instance:

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

Chi tiết: [docs/BENCHMARKS.vi.md](docs/BENCHMARKS.vi.md).

## Security

Luồng mặc định là localhost với `ENABLE_CLOUDFLARE_TUNNEL=False`. Khi bật public tunnel, bắt buộc có `QWEN3VL_API_KEY`; public request cần Bearer token, còn localhost không cần key. Không được in hoặc commit secret.

Xem [docs/SECURITY.vi.md](docs/SECURITY.vi.md).

## Verification

```bash
pytest -q
python scripts/verify_asset_pack.py .
python scripts/verify_notebook.py notebooks/kaggle-production-showcase.ipynb
python -m compileall -q src scripts
```

Fresh local release-candidate gates cho catalog self-contained **23 assets / 19 case**: **40 tests PASS**, asset verifier PASS, notebook static verifier PASS (`34` cells, một showcase run), secret scan PASS (`64` text files), và canonical development evidence verifier PASS (`19/19` runtime cases).

## Các release gate còn lại

Trước public `v1.0.0`:

- chạy final production-showcase notebook trên tài khoản Kaggle chính thức và review toàn bộ free-form semantic output;
- promote official evidence đã duyệt vào `benchmarks/official/`;
- push local history lên GitHub và xác nhận public CI PASS.

Ngoài scope release đầu: custom web UI, Gradio/Streamlit, OpenAI-compatible API, `image_url`, base64 image input, quantization, vLLM/SGLang, multi-user account, persistent database và external production-cloud deployment.

## License và tài liệu

Code/tài liệu gốc của repository dùng [MIT](LICENSE). Model weights Qwen3-VL không được redistribute trong repo; người dùng attach riêng qua Kaggle. Upstream `Qwen/Qwen3-VL-8B-Instruct` dùng Apache-2.0; xem [LICENSE-NOTES.md](LICENSE-NOTES.md) để biết ranh giới attribution/license.

- [Kiến trúc](docs/ARCHITECTURE.vi.md)
- [REST API](docs/API.vi.md)
- [Kaggle](docs/KAGGLE.vi.md)
- [Benchmark](docs/BENCHMARKS.vi.md)
- [Bảo mật](docs/SECURITY.vi.md)
- [Đóng góp](CONTRIBUTING.vi.md)
- [Changelog](CHANGELOG.vi.md)
