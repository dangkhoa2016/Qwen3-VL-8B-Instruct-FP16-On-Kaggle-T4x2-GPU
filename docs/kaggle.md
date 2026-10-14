# Kaggle Execution Guide

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](kaggle.vi.md)

This guide assumes you may be new to Kaggle. It explains how to import the production-showcase notebook, select the required dual-T4 accelerator, attach the model, execute the notebook from a clean session, and interpret the final evidence.

## What Kaggle provides

Kaggle Notebooks are hosted Jupyter notebooks with a managed Python environment, temporary storage, optional Internet access, and configurable hardware accelerators. For this project, Kaggle is used as the reproducible execution environment for **two NVIDIA Tesla T4 GPUs**.

You do not need to install CUDA drivers or own a dual-GPU workstation locally.

## Before you start

You need:

- a Kaggle account with GPU access;
- enough available Kaggle GPU quota for a complete run;
- the notebook `notebooks/kaggle-production-showcase.ipynb`;
- the Kaggle model `dangkhoa2016/qwen-qwen3-vl-8b-instruct`;
- **GPU T4 ×2** selected as the accelerator;
- Internet enabled if the notebook must clone the GitHub repository.

The normal execution path does not require Cloudflare and does not require an external API client.

## Option A — use the Kaggle production-showcase notebook

Open:

[Qwen3-VL-8B FP16 T4x2 Production Showcase](https://www.kaggle.com/code/dangkhoa2016/qwen3-vl-8b-fp16-t4x2-production-showcase)

When the notebook is public, choose **Copy & Edit** to create an editable copy under your own account. The copy keeps the notebook structure while allowing you to configure your own accelerator, inputs, and saved versions.

If the notebook is still private during pre-release review, use Option B instead.

## Option B — import the `.ipynb` file

1. Clone or download this repository.
2. Locate `notebooks/kaggle-production-showcase.ipynb`.
3. Sign in to Kaggle.
4. Choose **Create → New Notebook**.
5. In the notebook editor choose **File → Import Notebook**.
6. Select `kaggle-production-showcase.ipynb`.

Kaggle occasionally changes menu labels. If the exact wording differs, use the notebook editor's import/upload function; the goal is to load the repository `.ipynb` as the current notebook source.

## Select GPU T4 ×2

In the notebook editor:

1. open **Settings**;
2. locate **Accelerator**;
3. select **GPU T4 ×2**.

The runtime expects exactly two visible NVIDIA Tesla T4 devices. It intentionally rejects CPU-only, single-T4, and incompatible GPU configurations instead of silently changing the runtime policy.

A correct environment should report two CUDA devices before model loading.

## Internet setting

Enable **Internet** when the notebook needs to clone the GitHub repository.

The model itself is loaded from the attached Kaggle Model, not downloaded as a second full checkpoint from Hugging Face. Therefore Internet is not required for inference once the required repository source and model attachment are already available in the environment.

## Attach the Qwen3-VL model

From the notebook editor:

1. open the **Input** pane;
2. choose **Add Input**;
3. search for `dangkhoa2016/qwen-qwen3-vl-8b-instruct`;
4. add the `Transformers / default / 1` variation.

The expected path is:

```text
/kaggle/input/models/dangkhoa2016/qwen-qwen3-vl-8b-instruct/transformers/default/1
```

Before running the model-loading cell, verify that this path exists. If it does not, remove and re-add the model input or confirm that the correct model variation was selected.

## Repository source

The notebook is designed to work from repository-controlled source. When source is not already available, its bootstrap clones the configured GitHub repository and resolves the requested ref.

For a clean official run, the notebook should print the resolved repository commit. This value is part of the provenance of the execution and should match the intended release candidate.

Do not treat a notebook run as authoritative if the resolved commit is stale or unexpected.

## Recommended clean-start procedure

Before **Run All**:

1. save any work you need from a previous session;
2. restart the Kaggle session if it has already loaded large models or run experimental code;
3. confirm **GPU T4 ×2** is still selected;
4. confirm Internet is enabled if a repository clone is required;
5. confirm the Kaggle model is attached;
6. leave `ENABLE_CLOUDFLARE_TUNNEL=False` for the first run;
7. use **Run All** from the top of the notebook.

Starting from a clean session reduces stale-process, VRAM, environment-variable, and source-provenance problems.

## What the notebook does

The production showcase is deliberately more than a basic inference example. A complete run performs the following sequence:

1. **Source/bootstrap verification** — identifies the repository URL, ref, and resolved commit.
2. **Hardware/software authority** — records Python, PyTorch, Transformers, Accelerate, CUDA, and both GPU identities.
3. **Configuration check** — keeps localhost as the default and Cloudflare optional.
4. **Asset verification** — checks the repository-controlled benchmark assets.
5. **REST server startup** — launches FastAPI/Uvicorn once on `127.0.0.1:8000`.
6. **Runtime identity gate** — verifies native FP16, SDPA, balanced dual-T4 placement, and no CPU/disk weight offload.
7. **REST examples** — demonstrates `/v1/generate`, `/v1/vision`, and `/v1/extract`.
8. **Canonical showcase** — executes all 19 canonical cases exactly once.
9. **Capability galleries** — renders stored results without repeating model inference.
10. **Service stability** — runs 12 additional requests on the same continuously loaded server instance.
11. **Metrics/dashboard** — summarizes latency, request counts, structured validation, and GPU memory.
12. **Final scorecard** — presents the execution identity and pass/review status in one place.

## Expected runtime identity

The intended runtime is:

```text
model: Qwen/Qwen3-VL-8B-Instruct
precision: torch.float16
attention: SDPA
device_map: balanced
GPU 0: NVIDIA Tesla T4
GPU 1: NVIDIA Tesla T4
max_memory GPU 0: 12 GiB
max_memory GPU 1: 12 GiB
CPU weight offload: false
Disk weight offload: false
```

Model sharding across two GPUs does not mean their VRAM is pooled into one contiguous device and does not mean requests are data-parallelized.

## Canonical showcase expectations

The notebook contains 19 canonical cases grouped into seven capabilities:

1. General Visual Understanding
2. Spatial & Relationship Reasoning
3. OCR & Document Understanding
4. Structured JSON Extraction
5. Tables & Visual Data Reasoning
6. Charts & Numerical Reasoning
7. Vietnamese & Multilingual

The canonical catalog is executed once. Later presentation sections reuse the stored results so the notebook does not accidentally benchmark duplicate inference work.

## Structured vs. free-form evaluation

Five structured cases have controlled expected fields and receive automatic semantic checks after:

1. JSON parsing;
2. schema validation;
3. strict expected-field comparison.

The normalization policy is intentionally narrow. Free-form responses are not automatically marked semantically correct simply because the HTTP request succeeded.

## Final scorecard

Before accepting a run, verify that the final scorecard includes:

- resolved repository commit;
- model identity and path;
- `torch.float16` dtype;
- both T4 GPU names;
- device map and offload flags;
- 19-case showcase status;
- structured parse/schema rates;
- structured semantic results;
- 12-request stability result;
- latency summary;
- Cloudflare enabled/disabled state.

Also inspect the actual free-form responses and rendered images. Automated runtime success is not a substitute for qualitative review.

## Saving a Kaggle version

After a successful run, use Kaggle's **Save Version** flow to preserve the notebook and its outputs.

Before making any notebook version public:

- review all cell outputs;
- confirm no token/API key is visible;
- confirm the resolved repository commit is correct;
- confirm the attached model is the intended variation;
- confirm no stale development provenance is being presented as final evidence.

## Optional Cloudflare Quick Tunnel

The default is:

```text
ENABLE_CLOUDFLARE_TUNNEL=False
```

If you explicitly want temporary public API access, set:

```text
ENABLE_CLOUDFLARE_TUNNEL=True
QWEN3VL_API_KEY=<secret>
```

Then start the tunnel only after the local service is ready. Tunnel startup fails closed if the API key is missing, and public-host requests require a Bearer token.

Never print or commit `QWEN3VL_API_KEY`.

## Troubleshooting

| Problem | Recommended check |
|---|---|
| Only one GPU is visible | reselect **GPU T4 ×2** in Settings and restart the session |
| Accelerator is unavailable | Kaggle GPU quota/account eligibility may be exhausted or temporarily unavailable |
| Model path does not exist | re-add `dangkhoa2016/qwen-qwen3-vl-8b-instruct`, variation `Transformers/default/1` |
| Repository clone fails | enable Internet or provide repository source another way |
| Runtime identity gate fails | confirm both GPUs are Tesla T4 and no unsupported environment override is set |
| Model loading OOMs after experiments | restart the session to release stale CUDA allocations and run from the top |
| CPU/disk appears in the device map | reject the run; this project intentionally forbids weight offload |
| `/v1/vision` rejects an upload | use JPEG/PNG/WEBP and stay within configured size/dimension limits |
| `/v1/extract` fails schema validation | inspect the raw model response; validation intentionally fails closed |
| Tunnel returns `401` | send `Authorization: Bearer <QWEN3VL_API_KEY>` |
| Notebook output differs after editing cells out of order | restart the session and use **Run All** |

For additional project-wide troubleshooting, see [troubleshooting.md](troubleshooting.md).

## Evidence handling

Generated session evidence belongs under `results/` and is intentionally ignored by Git. `benchmarks/official/` is the source-controlled official evidence index; reviewed runtime artifacts are published as an exact Kaggle execution/version plus matching GitHub Release assets and checksums.

Freeze the source SHA before the official execution. After that execution starts, do not rewrite the proven source history merely to add evidence files. This boundary prevents local development output, mocked CI output, or stale notebook output from being confused with official T4×2 evidence.
