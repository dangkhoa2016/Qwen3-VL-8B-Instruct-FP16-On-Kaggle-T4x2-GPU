# Benchmark và Evidence

Các số dưới đây là **development evidence trên Kaggle T4 x2 ngày 2026-10-14**, chưa được gọi là final public/official benchmark.

Runtime đã xác nhận: `Qwen3VLForConditionalGeneration`, `torch.float16`, SDPA, Tesla T4 x2, balanced device map, không CPU/disk offload.

Full showcase có 19 case: 3 general vision, 4 structured extraction, 4 OCR/document, 5 table/chart, 3 multilingual. Kết quả runtime **19/19 PASS**. Có 5 structured extraction case (tính cả Vietnamese case), JSON parse **100%**, schema validation **100%**, expected-field checks **5/5 PASS** sau normalization rất hẹp (NFKC + whitespace + dash typography). Các free-form response vẫn để reviewer đánh giá, không auto-PASS.

Service stability 12 request liên tiếp: **12/12 PASS**, 6 text + 3 vision + 3 extract; median wall latency 3,357 ms, max 15,482 ms; model identity không đổi; allocated CUDA memory delta **0 bytes trên cả hai GPU**; reserved delta +4 MiB mỗi GPU.

Chi tiết đầy đủ nằm trong `docs/BENCHMARKS.md`.
