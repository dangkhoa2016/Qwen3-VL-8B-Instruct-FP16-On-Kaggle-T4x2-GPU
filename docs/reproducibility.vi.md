# Reproducibility

> 🌐 Language / Ngôn ngữ: [English](reproducibility.md) | **Tiếng Việt**

Reproducibility yêu cầu model identity, runtime policy, assets và verification command phải rõ ràng.

1. Attach `Qwen/Qwen3-VL-8B-Instruct` vào Kaggle notebook thay vì tải checkpoint thứ hai.
2. Dùng hai Tesla T4, giữ `torch.float16`, SDPA, `device_map="balanced"`, batch 1 và giới hạn 12 GiB mỗi GPU.
3. Không bật CPU/disk weight offload hoặc quantization.
4. Verify assets bằng `python scripts/verify_asset_pack.py .`.
5. Chạy `pytest -q`, notebook static verification và secret scan trước publication.
6. Freeze và ghi lại exact source SHA trước official Kaggle run.
7. Xem `results/` là session output; publish reviewed official runtime evidence qua exact Kaggle version cùng GitHub Release assets/checksums tương ứng mà không rewrite frozen source history.
