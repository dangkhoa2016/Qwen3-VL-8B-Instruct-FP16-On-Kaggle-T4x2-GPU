# Qwen3-VL-8B-Instruct FP16 trên Kaggle T4×2 GPU

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

> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

Chạy **Qwen3-VL-8B-Instruct native FP16 trên hai GPU Tesla T4 của Kaggle** và sử dụng model như một multimodal REST service có thể tái sử dụng. Dự án kết hợp kiểm tra runtime nghiêm ngặt, FastAPI, schema-driven extraction, bộ dữ liệu kiểm thử đa phương thức được kiểm soát, evidence có thể tái lập và một Kaggle production showcase được thiết kế để người khác có thể kiểm chứng.

Repository này không chỉ là một ví dụ inference ngắn. Nó trình bày đầy đủ cách load model một lần, xác minh model thực sự được chia trên hai T4 mà không CPU/disk weight offload, phục vụ text/vision qua HTTP, trích xuất JSON có schema, theo dõi latency và GPU memory, đồng thời tái chạy toàn bộ quy trình trên Kaggle.

## Dự án cung cấp những gì

- **Qwen3-VL-8B-Instruct native FP16**, không GGUF và không quantization.
- **Kiểm tra nghiêm ngặt Tesla T4 ×2** với `device_map="balanced"` và ngân sách placement `12 GiB` cho mỗi GPU.
- **Không CPU hoặc disk weight offload**; startup fail rõ ràng thay vì âm thầm hạ cấu hình.
- **FastAPI REST service** cho text generation, vision understanding, structured extraction, runtime identity, health và metrics.
- **Multipart image upload** cho JPEG, PNG và WEBP; không fetch `image_url` phía server và không nhận ảnh base64.
- **Generic schema-driven JSON extraction** với JSON parse và schema validation.
- **19 canonical showcase cases** thuộc bảy nhóm capability.
- **Ví dụ tiếng Việt và đa ngôn ngữ** bên cạnh các case tiếng Anh.
- **12-request service stability qualification** trên cùng một server/model instance liên tục.
- **Cloudflare Quick Tunnel có xác thực, tùy chọn**, mặc định tắt.
- **Tài liệu song ngữ EN/VI**, hướng dẫn reproducibility, licensing và governance.

## Có thể kiểm thử những năng lực nào

| Năng lực | Ví dụ trong repository |
|---|---|
| Hiểu hình ảnh tổng quát | văn phòng, khu chợ, mô tả object và scene |
| Suy luận không gian & quan hệ | bố cục bãi xe, quan hệ giữa các vật thể trong quán cà phê |
| OCR & hiểu tài liệu | thông báo, warehouse summary, hiểu invoice/receipt ngoài transcription |
| Structured JSON extraction | invoice, receipt, business card, service form, phiếu giao hàng tiếng Việt |
| Bảng & visual data reasoning | bảng quarterly sales và delivery performance |
| Biểu đồ & numerical reasoning | support-ticket bar chart và satisfaction line chart |
| Tiếng Việt & multilingual | tài liệu tiếng Việt, nội dung EN/VI và câu hỏi chéo ngôn ngữ |

## Kiến trúc runtime

```text
Kaggle Notebook
    |
    | khởi động một local service process
    v
FastAPI + Uvicorn tại 127.0.0.1:8000
    |
    | load model đúng một lần
    v
Qwen/Qwen3-VL-8B-Instruct
FP16 + SDPA + balanced device map
    |
    +--> Tesla T4 GPU 0
    +--> Tesla T4 GPU 1
    |
    +--> REST client bên trong notebook
    +--> Cloudflare Quick Tunnel có xác thực, tùy chọn
```

Model được **shard trên hai GPU**. Đây không phải pooled VRAM và cũng không phải data parallelism. Runtime ưu tiên khả năng tái lập và an toàn bộ nhớ hơn throughput đồng thời, vì vậy chỉ có một inference request active tại một thời điểm.

## Cấu hình runtime

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

Loader xác minh đúng topology hai T4 và fail-closed nếu không thể giữ nguyên placement policy này.

## Chạy dự án trên Kaggle

Kaggle Notebooks là môi trường Jupyter notebook chạy trên cloud. Kaggle cung cấp Python environment, temporary storage và GPU accelerator, vì vậy bạn không cần một máy local có hai GPU T4 để chạy dự án này.

### 1. Tạo tài khoản Kaggle

Đăng nhập tại [kaggle.com](https://www.kaggle.com/). Khả năng sử dụng GPU phụ thuộc vào điều kiện tài khoản và quota của Kaggle.

### 2. Mở hoặc import notebook

Có hai cách:

**Cách A — bắt đầu từ Kaggle production showcase**

Mở:

[Qwen3-VL-8B FP16 T4x2 Production Showcase](https://www.kaggle.com/code/dangkhoa2016/qwen3-vl-8b-fp16-t4x2-production-showcase)

Khi notebook đã public, dùng **Copy & Edit** để tạo một bản có thể chỉnh sửa trong tài khoản Kaggle của bạn.

**Cách B — import notebook từ repository**

1. Download hoặc clone repository này.
2. Mở file `notebooks/kaggle-production-showcase.ipynb`.
3. Trên Kaggle chọn **Create → New Notebook**.
4. Trong notebook editor chọn **File → Import Notebook** rồi chọn file `.ipynb`.

Tên menu của Kaggle có thể thay đổi theo thời gian; mục tiêu cuối cùng là `kaggle-production-showcase.ipynb` trở thành notebook source trong session của bạn.

### 3. Chọn đúng accelerator

Trong notebook editor mở **Settings → Accelerator** và chọn **GPU T4 ×2**.

Dự án này cố ý yêu cầu đúng hai NVIDIA Tesla T4. CPU-only, T4 ×1 hoặc topology khác sẽ fail runtime identity gate thay vì tự chuyển sang cấu hình khác.

### 4. Bật Internet nếu notebook cần clone repository

Bootstrap notebook có thể clone GitHub repository khi source chưa có sẵn trong environment. Nếu dùng luồng này, bật **Internet** trong Kaggle notebook settings.

Nếu source đã có trong notebook environment thì bản thân model inference không cần Internet.

### 5. Attach Kaggle model

Trong notebook editor:

1. mở panel **Input**;
2. chọn **Add Input**;
3. tìm `dangkhoa2016/qwen-qwen3-vl-8b-instruct`;
4. thêm model variation `Transformers / default / 1`.

Model path mong đợi:

```text
/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1
```

Notebook sử dụng model đã attach từ Kaggle và **không** âm thầm tải thêm một full checkpoint thứ hai từ Hugging Face.

### 6. Giữ Cloudflare ở trạng thái tắt trong lần chạy đầu

Luồng bình thường là localhost-only:

```text
ENABLE_CLOUDFLARE_TUNNEL=False
```

Bạn không cần public tunnel để execute hoặc validate notebook.

### 7. Bắt đầu từ session sạch và Run All

Để kết quả dễ tái lập nhất:

1. restart Kaggle session nếu trước đó đã load model lớn khác;
2. xác nhận **GPU T4 ×2** vẫn đang được chọn;
3. xác nhận model đã attach;
4. chọn **Run All**.

Notebook sẽ:

1. xác minh repository/source identity;
2. xác minh môi trường hai T4;
3. xác minh showcase assets;
4. khởi động FastAPI service trên localhost;
5. chờ `/health` ready;
6. đọc `/v1/model` để chứng minh FP16 dual-T4 placement và không CPU/disk offload;
7. chạy REST API examples;
8. chạy 19 canonical showcase cases đúng một lần;
9. render lại kết quả đã lưu theo capability thay vì inference lại;
10. chạy 12-request service stability check;
11. hiển thị metrics, GPU memory snapshots, results dashboard và final scorecard.

### 8. Đọc final scorecard

Một run hợp lệ cần hiển thị các thông tin quan trọng như:

- resolved repository commit;
- model identity;
- dtype `torch.float16`;
- tên của cả hai Tesla T4;
- CPU/disk offload = false;
- trạng thái canonical showcase runtime;
- structured JSON parse/schema rates;
- structured semantic checks;
- service stability status;
- latency summary;
- Cloudflare status.

Không nên hiểu HTTP 200 là semantic quality tự động đúng. Free-form answers vẫn là model output cần review; chỉ những structured cases đã định nghĩa mới được automatic expected-field evaluation.

### 9. Lưu lại Kaggle run

Sau khi execute thành công, dùng **Save Version** nếu muốn lưu một notebook version có outputs. Luôn review outputs và secret trước khi public bất kỳ bản copy nào.

Hướng dẫn chi tiết hơn nằm tại [docs/kaggle.vi.md](docs/kaggle.vi.md).

## REST API

Base URL mặc định:

```text
http://127.0.0.1:8000
```

| Method | Endpoint | Mục đích |
|---|---|---|
| `GET` | `/health` | Liveness/readiness sau khi model initialize xong |
| `GET` | `/v1/model` | Model, dtype, attention, GPU placement và offload identity |
| `POST` | `/v1/generate` | Text-only generation |
| `POST` | `/v1/vision` | Image + prompt inference |
| `POST` | `/v1/extract` | Generic schema-driven extraction |
| `GET` | `/v1/metrics` | Request count, latency và CUDA memory snapshots |

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

Compact schema DSL hỗ trợ `string`, `number`, `integer`, `boolean`, nested object và array với một item schema. Tất cả object fields đều required và field dư do model sinh ra sẽ bị schema validation từ chối.

Guardrail mặc định gồm upload tối đa 10 MiB, chiều ảnh tối đa 4096 px, prompt tối đa 16.384 ký tự, schema tối đa 32 KiB và hard limit `max_new_tokens=2048`. Xem [docs/api.vi.md](docs/api.vi.md).

## Production showcase

Notebook execute **19 canonical cases đúng một lần** rồi tái sử dụng stored results cho gallery và dashboard. Catalog có bảy nhóm:

1. **General Visual Understanding**
2. **Spatial & Relationship Reasoning**
3. **OCR & Document Understanding**
4. **Structured JSON Extraction**
5. **Tables & Visual Data Reasoning**
6. **Charts & Numerical Reasoning**
7. **Vietnamese & Multilingual**

Năm structured cases có automatic semantic checks. Free-form vision/document answers được tách khỏi runtime success và vẫn cần human review nếu muốn đánh giá chất lượng.

## Development evidence đã xác minh

Các số liệu dưới đây được ghi nhận trong những T4×2 development runs đã verify. Đây là **development-session evidence**, không thay thế reviewed official evidence set được `benchmarks/official/` tham chiếu và publish qua exact Kaggle execution cùng GitHub Release assets tương ứng.

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

Một stability run riêng gồm 12 request trên cùng một continuously loaded server instance ghi nhận:

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

Repository cố ý tách ba khái niệm:

- **runtime success** — request/service đã execute thành công;
- **structured semantic checks** — field đã định nghĩa khớp expected values sau normalization nghiêm ngặt;
- **free-form quality** — cần human review và không auto-PASS chỉ vì HTTP request thành công.

Xem [docs/benchmarks.vi.md](docs/benchmarks.vi.md) và [docs/benchmark-methodology.vi.md](docs/benchmark-methodology.vi.md).

## Baseline acceptance và production showcase

Hai artifact này có vai trò khác nhau:

| Artifact | Mục đích |
|---|---|
| [Qwen3-VL-8B FP16 Kaggle T4×2 Production Acceptance](https://www.kaggle.com/code/dangkhoa2016/qwen3-vl-8b-fp16-kaggle-t4x2-production-acceptance) | Baseline qualification cho native FP16 viability, T4×2 placement, context/stability/OOM characterization và acceptance evidence |
| Repository này + `notebooks/kaggle-production-showcase.ipynb` | Reusable REST serving, deep multimodal cases, structured extraction, service metrics/stability và presentation-oriented evidence |

Production showcase bổ sung cho baseline acceptance notebook; nó không định nghĩa lại hoặc thay thế baseline acceptance criteria.

## Cloudflare Quick Tunnel tùy chọn

Localhost là mặc định được khuyến nghị. Nếu cần expose API tạm thời:

```text
ENABLE_CLOUDFLARE_TUNNEL=True
QWEN3VL_API_KEY=<secret>
```

Tunnel sẽ từ chối expose service nếu thiếu API key. Request qua public host phải gửi:

```text
Authorization: Bearer <QWEN3VL_API_KEY>
```

Localhost vẫn không yêu cầu auth. Không được in, lưu vào notebook output hoặc commit API key. Xem [docs/security.vi.md](docs/security.vi.md).

## Cấu trúc repository

```text
.github/                  CI, Dependabot, issue/PR templates và community health files
benchmarks/official/      chỉ chứa reviewed public benchmark artifacts
docs/                     architecture, API, Kaggle, benchmark, security và engineering guides
evidence/                 evidence policy và provenance boundary
examples/                 controlled multimodal assets
ground_truth/             canonical case catalog, schemas và expected facts
notebooks/                Kaggle production-showcase notebook
scripts/                  server, showcase, stability và verification helpers
src/qwen3vl_t4x2/         runtime, generation, API, metrics, security và evidence code
tests/                    unit, mocked và API-contract tests
```

## Chạy lại repository checks

```bash
pytest -q
python -m compileall -q src scripts
python scripts/verify_asset_pack.py .
python scripts/verify_notebook.py notebooks/kaggle-production-showcase.ipynb
python scripts/verify_no_secrets.py .
python scripts/verify_repository.py
```

CI chỉ dùng unit, mocked, API-contract, static và repository checks. CI **không** được trình bày như real GPU inference evidence.

## Xử lý sự cố thường gặp

| Hiện tượng | Cần kiểm tra |
|---|---|
| Model startup fail | model attachment, model path, hai Tesla T4 visible, VRAM khả dụng |
| Runtime chỉ thấy một GPU | kiểm tra **Settings → Accelerator → GPU T4 ×2**, sau đó restart session |
| Device map có CPU/disk | xem run là invalid; project cố ý không chấp nhận weight offload |
| Không thấy model path | add lại `dangkhoa2016/qwen-qwen3-vl-8b-instruct` từ Input pane |
| Clone repository fail | bật Internet cho clone path hoặc cung cấp repository source theo cách khác |
| `/v1/vision` từ chối ảnh | dùng JPEG/PNG/WEBP và tuân theo upload/dimension limits |
| `/v1/extract` từ chối output | xem raw model output; JSON/schema validation cố ý fail-closed |
| Tunnel trả `401` | thiết lập `QWEN3VL_API_KEY` và gửi Bearer token |
| Session không ổn định sau nhiều thử nghiệm | restart Kaggle session và Run All từ đầu |

Xem thêm [docs/troubleshooting.vi.md](docs/troubleshooting.vi.md).

## Tài liệu

- [Mục lục tài liệu](docs/index.vi.md) / [Documentation index](docs/index.md)
- [Kiến trúc](docs/architecture.vi.md) / [Architecture](docs/architecture.md)
- [REST API](docs/api.vi.md) / [REST API — EN](docs/api.md)
- [Hướng dẫn Kaggle](docs/kaggle.vi.md) / [Kaggle execution guide](docs/kaggle.md)
- [Benchmark](docs/benchmarks.vi.md) / [Benchmarks](docs/benchmarks.md)
- [Phương pháp benchmark](docs/benchmark-methodology.vi.md) / [Benchmark methodology](docs/benchmark-methodology.md)
- [Tái lập](docs/reproducibility.vi.md) / [Reproducibility](docs/reproducibility.md)
- [Xử lý sự cố](docs/troubleshooting.vi.md) / [Troubleshooting](docs/troubleshooting.md)
- [Bảo mật](docs/security.vi.md) / [Security](docs/security.md)
- [Giới hạn](docs/limitations.vi.md) / [Limitations](docs/limitations.md)
- [Đóng góp](CONTRIBUTING.vi.md) / [Contributing](CONTRIBUTING.md)
- [Changelog — VI](CHANGELOG.vi.md) / [Changelog](CHANGELOG.md)

## License và attribution

Source code và tài liệu gốc trong repository này được phát hành theo [MIT License](LICENSE), copyright **Đăng Khoa**.

Qwen3-VL model weights **không được redistribute trong repository này**. Model được attach riêng qua Kaggle. Upstream `Qwen/Qwen3-VL-8B-Instruct` sử dụng Apache-2.0; xem [MODEL_LICENSE.vi.md](MODEL_LICENSE.vi.md), [LICENSE-NOTES.vi.md](LICENSE-NOTES.vi.md) và [THIRD_PARTY_LICENSES/QWEN3-VL-APACHE-2.0.txt](THIRD_PARTY_LICENSES/QWEN3-VL-APACHE-2.0.txt).

Provenance và hash của showcase assets được ghi trong [LICENSE-SOURCES.vi.md](LICENSE-SOURCES.vi.md) và [ASSET_MANIFEST.json](ASSET_MANIFEST.json). Controlled release showcase không yêu cầu ảnh web bên thứ ba.
