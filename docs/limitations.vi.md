# Giới hạn

> 🌐 Language / Ngôn ngữ: [English](limitations.md) | **Tiếng Việt**

- Kaggle T4×2 là hai GPU độc lập; dự án không tuyên bố có pooled 32 GB VRAM.
- Service cố ý serialize inference để reproducible và an toàn bộ nhớ; đây không phải high-throughput serving benchmark.
- Strict release baseline không hỗ trợ quantization, CPU offload hoặc disk offload.
- Chất lượng VLM free-form có thể thay đổi theo độ mơ hồ của ảnh. Trong development, một grouped-bar exact-difference case cho thấy reasoning weakness thật và đã bị loại khỏi default catalog thay vì tune prompt đến khi PASS.
- Development measurements chưa phải official public benchmark evidence cho tới khi reproduce và review trên tài khoản Kaggle chính thức.
