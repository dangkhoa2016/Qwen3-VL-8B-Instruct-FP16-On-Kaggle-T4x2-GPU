# Kiến trúc

Repository này là lớp production-style showcase cho Qwen3-VL-8B-Instruct FP16 trên Kaggle Tesla T4 x2. Notebook acceptance đã công bố trước đó vẫn là nguồn chứng cứ baseline; repository này tập trung vào REST service tái sử dụng và showcase multimodal sâu.

## Luồng chạy

Notebook khởi động một FastAPI/Uvicorn server tại `127.0.0.1:8000`. Server load model đúng một lần với FP16, SDPA, balanced device map trên hai GPU T4. Notebook sau đó chỉ tương tác qua HTTP. Cloudflare Quick Tunnel là tùy chọn và tắt mặc định.

## Các bất biến runtime

Startup phải fail rõ ràng nếu không giữ được baseline:

- đúng hai Tesla T4;
- floating weights chỉ ở `torch.float16`;
- SDPA;
- `device_map="balanced"`, budget `12GiB` mỗi GPU;
- weights phải nằm trên cả GPU 0 và GPU 1;
- không CPU weight offload;
- không disk weight offload;
- không reload model theo request.

## API

Các endpoint: `/health`, `/v1/model`, `/v1/generate`, `/v1/vision`, `/v1/extract`, `/v1/metrics`. Image chỉ nhận multipart upload; không hỗ trợ URL hoặc base64.

## Evidence

HTTP PASS không đồng nghĩa quality PASS. Free-form vision cần reviewer xem; structured extraction chỉ PASS tự động sau JSON parse, schema validation và expected-field check.
