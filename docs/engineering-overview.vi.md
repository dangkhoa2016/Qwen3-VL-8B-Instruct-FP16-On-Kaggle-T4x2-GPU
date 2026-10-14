# Tổng quan engineering

> 🌐 Language / Ngôn ngữ: [English](engineering-overview.md) | **Tiếng Việt**

Repository biến một lần load model thành service có thể review, thay vì giấu toàn bộ logic trong một notebook cell.

Các ưu tiên engineering gồm: giữ đúng FP16 identity, placement rõ ràng trên hai T4, không weight offload, một model instance sống lâu, REST endpoint chuyên biệt, schema-validated extraction, local-first security, assets reproducible và evidence tách transport success khỏi semantic quality.

Acceptance notebook vẫn là baseline qualification authority; repository này tập trung vào reusable serving và multimodal demonstrations sâu hơn.
