# Phương pháp benchmark

> 🌐 Language / Ngôn ngữ: [English](benchmark-methodology.md) | **Tiếng Việt**

Dự án tách riêng **runtime success**, **structured semantic validation** và **manual free-form review**. HTTP 200 không bao giờ tự động được xem là quality PASS.

## Quy tắc đo

- Ghi wall latency theo từng case từ phía client.
- Ghi model identity, dtype, số GPU và trạng thái offload cho mỗi campaign.
- Với `/v1/extract`, JSON phải parse và pass JSON-Schema trước semantic check.
- Chỉ so các field được khai báo trong ground truth; không âm thầm sửa output model.
- Vision/OCR free-form được review thủ công với expected facts.
- Median/min/max phải lấy từ records của chính campaign, không lấy cumulative server metrics.

## Development campaign

Campaign development đã review hiện có 19 case release-candidate thuộc general vision, structured extraction, OCR/document, tables/charts và multilingual. Đây vẫn là development evidence cho tới khi official Kaggle run từ frozen source SHA được review và publish thành authoritative evidence set.
