# Troubleshooting

> 🌐 Language / Ngôn ngữ: [English](troubleshooting.md) | **Tiếng Việt**

| Triệu chứng | Kiểm tra |
|---|---|
| Model startup fail | attached model path, hai T4 visible, VRAM trống |
| Device map có CPU/disk | fail run; không âm thầm chấp nhận offload |
| `/v1/vision` reject upload | MIME JPEG/PNG/WEBP và giới hạn size/dimension |
| `/v1/extract` invalid structured output | xem raw output; schema validation cố ý fail-closed |
| Public tunnel trả 401 | đặt `QWEN3VL_API_KEY` và gửi Bearer auth |
| Local API đòi auth | dùng `127.0.0.1` hoặc `localhost`; public-host policy khác |
| Benchmark answer mơ hồ | kiểm tra asset/prompt; không chỉnh evaluator chỉ để ép PASS |

Khi điều tra GPU/OOM, hãy lưu `/v1/model`, `/v1/metrics`, prompt chính xác và case ID.
