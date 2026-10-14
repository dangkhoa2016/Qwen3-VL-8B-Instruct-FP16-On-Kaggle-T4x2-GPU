# Mô hình bảo mật

> 🌐 Language / Ngôn ngữ: [English](security.md) | **Tiếng Việt**


Đây là Kaggle demo/reference implementation, không phải dịch vụ internet multi-tenant đã harden.

Mặc định server bind `127.0.0.1`, Cloudflare tunnel tắt, localhost không cần API key. Nếu bật tunnel mà thiếu `QWEN3VL_API_KEY`, startup phải fail-closed. Public host dùng Bearer token và constant-time comparison.

Upload chỉ nhận JPEG/PNG/WEBP qua multipart, có giới hạn dung lượng/kích thước; không fetch URL từ server và không nhận base64. Prompt/schema/output-token đều có limit. Inference được serialize bằng global lock để giảm rủi ro OOM.
