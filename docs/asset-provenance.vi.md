# Provenance của assets

> 🌐 Language / Ngôn ngữ: [English](asset-provenance.md) | **Tiếng Việt**

Release catalog là self-contained và không phụ thuộc ảnh ngẫu nhiên trên Internet.

- `examples/realistic/`: sáu JPEG photorealistic do AI tạo riêng cho dự án, resize 1024×768.
- các thư mục `examples/` còn lại: PNG controlled được tạo bằng chương trình từ dữ liệu benchmark hư cấu.
- `ASSET_MANIFEST.json`: SHA-256 và generation class.
- `ground_truth/cases.json`: prompt, expected facts và structured schemas.

Tên tổ chức và identifier hư cấu giúp tránh làm người xem hiểu nhầm benchmark documents là hồ sơ thương mại thật.
