# Hướng dẫn chạy trên Kaggle

> 🌐 Language / Ngôn ngữ: [English](kaggle.md) | **Tiếng Việt**

Tài liệu này dành cả cho người chưa từng sử dụng Kaggle. Nó hướng dẫn từ bước import production-showcase notebook, chọn đúng GPU T4 ×2, attach model, chạy notebook từ một session sạch cho tới cách đọc final evidence.

## Kaggle cung cấp những gì

Kaggle Notebooks là Jupyter notebook chạy trên cloud, có sẵn Python environment, temporary storage, tùy chọn Internet và hardware accelerator. Trong dự án này, Kaggle được dùng như execution environment có thể tái lập với **hai NVIDIA Tesla T4**.

Bạn không cần tự cài CUDA driver và cũng không cần sở hữu máy local có hai GPU T4.

## Cần chuẩn bị gì

Bạn cần:

- tài khoản Kaggle có quyền dùng GPU;
- GPU quota còn đủ cho một full run;
- notebook `notebooks/kaggle-production-showcase.ipynb`;
- Kaggle model `dangkhoa2016/qwen-qwen3-vl-8b-instruct`;
- accelerator **GPU T4 ×2**;
- Internet nếu notebook cần clone GitHub repository.

Luồng chạy mặc định không cần Cloudflare và không cần external API client.

## Cách A — dùng Kaggle production-showcase notebook

Mở:

[Qwen3-VL-8B FP16 T4x2 Production Showcase](https://www.kaggle.com/code/dangkhoa2016/qwen3-vl-8b-fp16-t4x2-production-showcase)

Khi notebook đã public, chọn **Copy & Edit** để tạo một bản editable trong tài khoản của bạn. Bản copy giữ cấu trúc notebook nhưng cho phép bạn tự cấu hình accelerator, input và saved version.

Nếu notebook còn private trong giai đoạn pre-release review, hãy dùng Cách B.

## Cách B — import file `.ipynb`

1. Clone hoặc download repository này.
2. Tìm `notebooks/kaggle-production-showcase.ipynb`.
3. Đăng nhập Kaggle.
4. Chọn **Create → New Notebook**.
5. Trong notebook editor chọn **File → Import Notebook**.
6. Chọn file `kaggle-production-showcase.ipynb`.

Kaggle có thể thay đổi tên menu theo thời gian. Nếu wording khác, hãy dùng chức năng import/upload notebook của editor; mục tiêu là đưa file `.ipynb` của repository thành notebook source hiện tại.

## Chọn GPU T4 ×2

Trong notebook editor:

1. mở **Settings**;
2. tìm mục **Accelerator**;
3. chọn **GPU T4 ×2**.

Runtime yêu cầu đúng hai NVIDIA Tesla T4 visible. Project cố ý từ chối CPU-only, T4 ×1 hoặc GPU topology không phù hợp thay vì âm thầm đổi runtime policy.

Một environment đúng cần báo hai CUDA devices trước khi load model.

## Thiết lập Internet

Bật **Internet** nếu notebook cần clone GitHub repository.

Model được load từ Kaggle Model đã attach, không tải một full checkpoint thứ hai từ Hugging Face. Vì vậy sau khi repository source và model attachment đã sẵn sàng, bản thân inference không phụ thuộc Internet.

## Attach Qwen3-VL model

Trong notebook editor:

1. mở panel **Input**;
2. chọn **Add Input**;
3. tìm `dangkhoa2016/qwen-qwen3-vl-8b-instruct`;
4. add variation `Transformers / default / 1`.

Path mong đợi:

```text
/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1
```

Trước cell load model, hãy xác nhận path này tồn tại. Nếu không có, remove/add lại model input hoặc kiểm tra đã chọn đúng variation chưa.

## Repository source

Notebook được thiết kế chạy từ repository-controlled source. Khi source chưa có sẵn, bootstrap sẽ clone GitHub repository theo URL/ref đã cấu hình.

Trong một clean official run, notebook phải in ra resolved repository commit. SHA này là một phần của provenance và phải khớp release candidate dự kiến.

Không nên coi run là authoritative nếu resolved commit bị stale hoặc không đúng mong đợi.

## Quy trình clean start được khuyến nghị

Trước **Run All**:

1. lưu lại dữ liệu cần thiết từ session cũ;
2. restart Kaggle session nếu trước đó đã load large model hoặc chạy experimental code;
3. xác nhận **GPU T4 ×2** vẫn được chọn;
4. xác nhận Internet đã bật nếu cần clone repository;
5. xác nhận Kaggle model đã attach;
6. giữ `ENABLE_CLOUDFLARE_TUNNEL=False` cho lần chạy đầu;
7. dùng **Run All** từ đầu notebook.

Session sạch giúp tránh stale process, VRAM allocation cũ, environment variable cũ và source provenance không rõ ràng.

## Notebook sẽ làm gì

Production showcase không chỉ là basic inference. Một full run thực hiện:

1. **Source/bootstrap verification** — ghi repository URL, ref và resolved commit.
2. **Hardware/software authority** — ghi Python, PyTorch, Transformers, Accelerate, CUDA và hai GPU identity.
3. **Configuration check** — localhost mặc định, Cloudflare tùy chọn.
4. **Asset verification** — kiểm tra repository-controlled benchmark assets.
5. **REST server startup** — launch FastAPI/Uvicorn một lần trên `127.0.0.1:8000`.
6. **Runtime identity gate** — xác minh native FP16, SDPA, balanced dual-T4 placement và không CPU/disk offload.
7. **REST examples** — minh họa `/v1/generate`, `/v1/vision`, `/v1/extract`.
8. **Canonical showcase** — chạy đủ 19 canonical cases đúng một lần.
9. **Capability galleries** — render stored results, không inference lặp lại.
10. **Service stability** — chạy 12 request bổ sung trên cùng continuously loaded server instance.
11. **Metrics/dashboard** — tổng hợp latency, request count, structured validation và GPU memory.
12. **Final scorecard** — trình bày execution identity và pass/review status tập trung.

## Runtime identity mong đợi

```text
model: Qwen/Qwen3-VL-8B-Instruct
precision: torch.float16
attention: SDPA
device_map: balanced
GPU 0: NVIDIA Tesla T4
GPU 1: NVIDIA Tesla T4
max_memory GPU 0: 12 GiB
max_memory GPU 1: 12 GiB
CPU weight offload: false
Disk weight offload: false
```

Model sharding trên hai GPU không có nghĩa VRAM được pool thành một device liên tục và cũng không phải request data parallelism.

## Kỳ vọng của canonical showcase

Notebook có 19 canonical cases thuộc bảy nhóm:

1. General Visual Understanding
2. Spatial & Relationship Reasoning
3. OCR & Document Understanding
4. Structured JSON Extraction
5. Tables & Visual Data Reasoning
6. Charts & Numerical Reasoning
7. Vietnamese & Multilingual

Canonical catalog chỉ chạy một lần. Các presentation sections phía sau dùng stored results để tránh benchmark trùng inference work.

## Structured evaluation và free-form evaluation

Năm structured cases có controlled expected fields và được automatic semantic check sau:

1. JSON parsing;
2. schema validation;
3. strict expected-field comparison.

Normalization policy cố ý hẹp. Free-form response không được auto-mark semantic PASS chỉ vì HTTP request thành công.

## Kiểm tra final scorecard

Trước khi chấp nhận một run, hãy xác minh final scorecard có:

- resolved repository commit;
- model identity và path;
- dtype `torch.float16`;
- tên của cả hai T4;
- device map và offload flags;
- trạng thái 19-case showcase;
- structured parse/schema rates;
- structured semantic results;
- kết quả 12-request stability;
- latency summary;
- Cloudflare enabled/disabled state.

Ngoài ra phải review actual free-form responses và rendered images. Automated runtime success không thay thế qualitative review.

## Lưu một Kaggle version

Sau khi run thành công, dùng **Save Version** để lưu notebook và outputs.

Trước khi public bất kỳ notebook version nào:

- review toàn bộ cell outputs;
- xác nhận không có token/API key bị lộ;
- xác nhận resolved repository commit chính xác;
- xác nhận model attachment đúng variation;
- xác nhận stale development provenance không bị trình bày như final evidence.

## Cloudflare Quick Tunnel tùy chọn

Mặc định:

```text
ENABLE_CLOUDFLARE_TUNNEL=False
```

Nếu thực sự cần public API tạm thời:

```text
ENABLE_CLOUDFLARE_TUNNEL=True
QWEN3VL_API_KEY=<secret>
```

Chỉ start tunnel sau khi local service ready. Tunnel fail-closed nếu thiếu API key và public-host request phải có Bearer token.

Không được in hoặc commit `QWEN3VL_API_KEY`.

## Troubleshooting

| Vấn đề | Cần kiểm tra |
|---|---|
| Chỉ thấy một GPU | chọn lại **GPU T4 ×2** trong Settings rồi restart session |
| Accelerator không khả dụng | GPU quota/account eligibility của Kaggle có thể hết hoặc tạm unavailable |
| Model path không tồn tại | add lại `dangkhoa2016/qwen-qwen3-vl-8b-instruct`, variation `Transformers/default/1` |
| Clone repository fail | bật Internet hoặc cung cấp repository source theo cách khác |
| Runtime identity gate fail | xác nhận cả hai GPU là Tesla T4 và không có unsupported environment override |
| Model OOM sau nhiều experiment | restart session để giải phóng stale CUDA allocations rồi Run All từ đầu |
| Device map có CPU/disk | reject run; project cố ý cấm weight offload |
| `/v1/vision` reject upload | dùng JPEG/PNG/WEBP và tuân theo size/dimension limits |
| `/v1/extract` fail schema | xem raw model response; validation cố ý fail-closed |
| Tunnel trả `401` | gửi `Authorization: Bearer <QWEN3VL_API_KEY>` |
| Output khác thường sau khi chạy cell không theo thứ tự | restart session rồi dùng **Run All** |

Xem thêm [troubleshooting.vi.md](troubleshooting.vi.md).

## Quản lý evidence

Session evidence được tạo dưới `results/` và cố ý bị Git ignore. `benchmarks/official/` là source-controlled official evidence index; reviewed runtime artifacts được publish dưới exact Kaggle execution/version cùng GitHub Release assets và checksums tương ứng.

Hãy freeze source SHA trước official execution. Sau khi execution đó bắt đầu, không rewrite proven source history chỉ để bổ sung evidence files. Ranh giới này giúp tránh nhầm local development output, mocked CI output hoặc stale notebook output thành official T4×2 evidence.
