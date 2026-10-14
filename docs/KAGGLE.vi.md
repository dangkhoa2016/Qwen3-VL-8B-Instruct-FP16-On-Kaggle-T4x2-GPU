# Hướng dẫn Kaggle

1. Tạo/mở Kaggle Notebook.
2. Chọn **GPU T4 x2**.
3. Attach model `dangkhoa2016/qwen-qwen3-vl-8b-instruct`.
4. Kiểm tra path `/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1`.
5. Chạy `notebooks/kaggle-production-showcase.ipynb`.

Notebook không tải thêm một full checkpoint từ Hugging Face. Luồng mặc định chỉ dùng localhost; Cloudflare tunnel tắt mặc định. Evidence session nằm trong `results/` và không commit tự động. Chỉ sau khi official Kaggle run được review mới promote artifact sang `benchmarks/official/`.
