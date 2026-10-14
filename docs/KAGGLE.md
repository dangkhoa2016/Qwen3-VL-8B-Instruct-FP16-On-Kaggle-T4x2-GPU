# Kaggle Execution Guide

## Requirements

1. Open a Kaggle Notebook.
2. Select **GPU T4 x2**.
3. Attach Kaggle Model `dangkhoa2016/qwen-qwen3-vl-8b-instruct`.
4. Confirm the expected path exists:
   `/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1`.
5. Use `notebooks/kaggle-production-showcase.ipynb`.

The notebook deliberately does not download a second full checkpoint from Hugging Face.

## Default execution

The notebook verifies hardware and assets, starts the localhost REST server, waits for readiness, audits `/v1/model`, runs one text smoke test, executes the multimodal catalog once, renders evidence by capability, performs a 12-request service stability check, and prints the final summary.

## Optional tunnel

Keep `ENABLE_CLOUDFLARE_TUNNEL=False` for normal execution. To opt in, provide `QWEN3VL_API_KEY` without printing it and run `scripts/start_cloudflare_tunnel.sh` after the local service is ready.

## Evidence

Generated session evidence is written under `results/` and is intentionally ignored by Git. Public benchmark artifacts should be promoted deliberately to `benchmarks/official/` only after an official Kaggle run is reviewed.
