# License Notes and Upstream Attribution

The repository's original code and documentation are released under the MIT License.

## Upstream Qwen3-VL model

This repository uses **Qwen/Qwen3-VL-8B-Instruct** through a separately attached Kaggle Model. Model weights are **not redistributed by this repository**.

The authoritative upstream model page and Qwen3-VL source repository were re-verified on **2026-10-14** and both identify the upstream license as **Apache License 2.0**:

- https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
- https://github.com/QwenLM/Qwen3-VL

The local Kaggle mirror is only a transport/attachment used for inference. Upstream model rights and obligations remain governed by the upstream Apache-2.0 terms; this repository's MIT license does not relicense the model weights.

## Assets

All image assets required by the release showcase are project-generated; no third-party web photograph is required.

- Six photorealistic JPEG assets in `examples/realistic/` were generated specifically for this project using OpenAI image generation and resized to 1024×768.
- Remaining benchmark images were generated programmatically from fictional data for controlled evaluation.
- Asset hashes and generation class are recorded in `ASSET_MANIFEST.json`.

See `LICENSE-SOURCES.md` for the release asset policy and provenance summary.
