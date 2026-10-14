# Chính sách bảo mật

> 🌐 Language / Ngôn ngữ: [English](SECURITY.md) | **Tiếng Việt**

## Tư thế runtime

FastAPI service mặc định bind localhost. Cloudflare Quick Tunnel là optional và tắt mặc định. Khi bật public exposure, bắt buộc có `QWEN3VL_API_KEY` và public-host request cần Bearer authentication.

Implementation fail-closed nếu bật tunnel nhưng thiếu key. Không được in hoặc commit secret.

## Báo cáo

Không đăng credential, private data hoặc exploit detail trong issue công khai. Hãy báo riêng cho chủ repository qua contact trên GitHub profile, kèm commit bị ảnh hưởng, bước tái hiện và impact.

Xem [docs/security.vi.md](docs/security.vi.md) để biết threat model chi tiết.
