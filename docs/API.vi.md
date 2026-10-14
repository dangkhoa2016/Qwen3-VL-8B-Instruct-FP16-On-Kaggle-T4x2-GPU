# REST API

Base URL mặc định: `http://127.0.0.1:8000`.

Các endpoint gồm `/health`, `/v1/model`, `/v1/generate`, `/v1/vision`, `/v1/extract`, `/v1/metrics`.

`/v1/vision` và `/v1/extract` chỉ nhận ảnh bằng multipart upload (JPEG/PNG/WEBP), không nhận `image_url` hay base64. `/v1/extract` dùng compact schema DSL với các kiểu `string`, `number`, `integer`, `boolean`, object lồng nhau và array một item-schema.

Structured extraction chỉ trả success khi output parse được JSON và pass normalized-schema validation. Metrics không tự tính request `/v1/metrics` hiện tại vào snapshot để số `total/success` không lệch nhau.

Khi Cloudflare tunnel được bật, request public cần `Authorization: Bearer <QWEN3VL_API_KEY>`. Localhost không yêu cầu key; tunnel fail-closed nếu thiếu key.

Xem `docs/API.md` để có đầy đủ ví dụ `curl` có thể copy trực tiếp.
