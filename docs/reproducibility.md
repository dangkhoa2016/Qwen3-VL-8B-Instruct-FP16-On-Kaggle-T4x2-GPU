# Reproducibility

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](reproducibility.vi.md)

Reproducibility depends on keeping model identity, runtime policy, assets and verification commands explicit.

1. Attach `Qwen/Qwen3-VL-8B-Instruct` to the Kaggle notebook rather than downloading a second checkpoint.
2. Use two Tesla T4 GPUs and keep `torch.float16`, SDPA, `device_map="balanced"`, batch 1 and 12 GiB max-memory caps per GPU.
3. Do not enable CPU/disk weight offload or quantization.
4. Verify assets with `python scripts/verify_asset_pack.py .`.
5. Run `pytest -q`, notebook static verification and secret scan before publication.
6. Freeze and record the exact source SHA before the official Kaggle run.
7. Treat `results/` as session output; publish reviewed official runtime evidence through the exact Kaggle version and matching GitHub Release assets/checksums without rewriting the frozen source history.
