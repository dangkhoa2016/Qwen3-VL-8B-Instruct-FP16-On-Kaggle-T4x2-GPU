# Nguồn assets và giấy phép

> 🌐 Language / Ngôn ngữ: [English](LICENSE-SOURCES.md) | **Tiếng Việt**

Toàn bộ ảnh dùng trong release showcase do dự án tạo; không cần ảnh lấy ngẫu nhiên từ Internet.

## Ảnh photorealistic do AI tạo

Sáu file JPEG trong `examples/realistic/` được tạo riêng cho dự án bằng OpenAI image generation và resize về 1024×768. Đây là benchmark image synthetic, không phải ảnh tải từ web.

## Assets tạo bằng chương trình

Các file PNG benchmark còn lại được tạo riêng cho repository từ dữ liệu hư cấu có kiểm soát.

## Kiểm soát provenance

`ASSET_MANIFEST.json` lưu SHA-256 và generation class. Nếu tương lai bổ sung asset bên thứ ba, cần ghi source URL, author, license, lịch sử chỉnh sửa và cơ sở redistribution trước khi merge.
