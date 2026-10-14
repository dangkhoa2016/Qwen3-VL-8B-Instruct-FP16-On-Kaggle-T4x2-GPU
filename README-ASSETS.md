# Qwen3-VL 8B Kaggle T4×2 — Showcase Assets

The release asset set is intentionally self-contained and contains **no required third-party web photographs**.

## Asset classes

- `examples/realistic/`: six AI-generated photorealistic JPEG benchmark assets created specifically for this project and resized to 1024×768.
- other `examples/` directories: deterministic programmatically generated documents, charts, tables and controlled visual scenes.

`ASSET_MANIFEST.json` records dimensions, generation class and SHA-256 for every release image. `ground_truth/cases.json` defines endpoint, prompt/schema and expected facts.

## Current catalog

The release catalog contains 19 runnable cases across five groups: general vision, OCR/document understanding, structured extraction, tables/charts, and multilingual mixed-context vision.

## Evidence rule

HTTP 200 is runtime evidence only. Structured extraction additionally requires JSON parse, schema validation and expected-field checks. Free-form vision/document/chart answers remain reviewer-inspected.
