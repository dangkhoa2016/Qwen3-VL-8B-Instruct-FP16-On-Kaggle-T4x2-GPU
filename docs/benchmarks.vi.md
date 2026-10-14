# Benchmark và Evidence

> 🌐 Language / Ngôn ngữ: [English](benchmarks.md) | **Tiếng Việt**


Các số dưới đây là **development evidence trên Kaggle T4 x2 ngày 2026-10-14**, chưa được gọi là final public/official benchmark.

Runtime đã xác nhận: `Qwen3VLForConditionalGeneration`, `torch.float16`, SDPA, Tesla T4 x2, balanced device map, không CPU/disk offload.

## Photorealistic showcase 19 case

Catalog release hiện tại hoàn toàn self-contained với **19 case**: 4 general vision, 4 structured extraction, 4 OCR/document, 4 table/chart và 3 multilingual. Một case multilingual cũng gọi `/v1/extract`, nên tổng số structured endpoint case là **5**. Sáu input reviewer-facing là ảnh photorealistic do AI tạo riêng cho dự án: office, waterfront produce market, invoice, receipt, business card và poster EN/VI; release không cần ảnh web bên thứ ba.

Final development campaign của đúng asset/catalog/prompt hiện tại đạt:

- runtime **19/19 PASS**;
- JSON parse **100%** trên 5 structured endpoint case;
- schema validation **100%**;
- expected-field checks **5/5 PASS** sau normalization rất hẹp (NFKC + collapse whitespace + tương đương dash typography);
- **14/14 free-form case đã được manual review** và chứa các expected facts; evidence engine vẫn không tự gắn semantic PASS cho free-form chỉ vì HTTP 200.

Wall latency theo từng record của campaign này: median **13,822 ms**, min **5,356 ms**, max **32,115 ms**. Đây là deep showcase, không phải throughput benchmark.

## Curation minh bạch

Trong development review, câu hỏi crossing-point trên line chart cho thấy một reasoning inconsistency thật: model đọc đúng `A=61`, `B=63` ở W3 nhưng vẫn mô tả A lớn hơn B. Release showcase không che lỗi này bằng evaluator tolerance; case giữ lại chuyển sang bài đọc numeric label + arithmetic difference rõ ràng.

Một grouped-bar exact-difference probe cũng bị loại khỏi default release catalog sau khi model tiếp tục suy luận sai category/sign dù chart đã có numeric labels. Asset vẫn được giữ, nhưng failure probe đó không được trình bày như release quality PASS.

## Service stability

Service stability 12 request liên tiếp trên cùng model/server instance: **12/12 PASS**, gồm 6 text + 3 vision + 3 extract; median wall latency 3,357 ms, max 15,482 ms; model identity không đổi; allocated CUDA memory delta **0 bytes trên cả hai GPU**; reserved delta +4 MiB mỗi GPU.

Chi tiết phương pháp và caveat đầy đủ nằm trong `docs/benchmarks.md`.
