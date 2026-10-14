# Đóng góp

> 🌐 Language / Ngôn ngữ: [English](CONTRIBUTING.md) | **Tiếng Việt**

Mọi contribution cần nhỏ, dễ review và không làm sai lệch evidence.

## Quy tắc development

- Thêm/cập nhật test trước khi đổi behavior.
- Giữ strict FP16/T4×2/no-offload baseline trừ khi thay đổi tạo một mode riêng được document rõ.
- Tách runtime success khỏi semantic quality evaluation.
- Không gọi output mock từ GitHub Actions là evidence GPU Kaggle thật.
- Đồng bộ tài liệu English/Vietnamese.
- Không commit API key, Kaggle/Hugging Face credential hoặc tunnel secret.

## Kiểm chứng local

Chạy `pytest -q`, `python -m compileall -q src scripts`, asset verification, notebook verification, repository audit và secret scan trước khi đề xuất merge.
