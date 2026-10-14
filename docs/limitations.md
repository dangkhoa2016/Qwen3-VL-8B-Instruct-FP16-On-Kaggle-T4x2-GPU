# Limitations

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](limitations.vi.md)

- Kaggle T4×2 is two independent GPUs; this project does not claim pooled 32 GB VRAM.
- The service intentionally serializes inference for reproducibility and memory safety; it is not a high-throughput serving benchmark.
- No quantization, CPU offload or disk offload path is supported by the strict release baseline.
- Free-form VLM quality can vary with visual ambiguity. During development, a grouped-bar exact-difference case exposed a real reasoning weakness and was removed from the default release catalog rather than prompt-tuned until it passed.
- Development measurements are not official public benchmark evidence until reproduced and reviewed on the official Kaggle account.
