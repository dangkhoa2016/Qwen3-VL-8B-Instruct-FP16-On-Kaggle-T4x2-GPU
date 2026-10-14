# Benchmarks and Evidence

## Evidence status

The numbers below are **development evidence from the current Kaggle T4 x2 implementation session on 2026-10-14**. They are not yet labeled as the final public/official Kaggle benchmark. Official release documentation must be refreshed from the reviewed public production-showcase execution.

## Runtime identity observed

- architecture: `Qwen3VLForConditionalGeneration`;
- dtype: `torch.float16`;
- attention: SDPA;
- GPUs: Tesla T4 x2;
- device map strategy: balanced;
- CPU weight offload: false;
- disk weight offload: false.

Observed placement put the visual module, embeddings and language layers 0-13 on GPU 0; layers 14-35 plus final language components and `lm_head` were on GPU 1.

## 19-case showcase campaign

The default local asset catalog contained 19 runnable cases across five capability groups:

| Capability | Cases |
|---|---:|
| General vision | 3 |
| Structured extraction | 4 |
| OCR/document understanding | 4 |
| Tables/charts | 5 |
| Multilingual | 3 |
| **Total** | **19** |

Measured development result:

- runtime success: **19/19**;
- structured cases (including the Vietnamese extraction case): **5**;
- JSON parse rate: **100%**;
- schema validation rate: **100%**;
- expected-field semantic checks: **5/5 PASS** after a deliberately narrow text normalization (`NFKC`, whitespace collapse, typographic-dash equivalence only);
- free-form vision/document/chart answers remain manual semantic review and are not auto-labeled quality PASS.

Server metrics at the end of this campaign showed 21 tracked requests (health/model plus 14 vision and 5 extraction), median request latency 29,725 ms and p95 45,541 ms. These aggregate latencies reflect deliberately deep prompts and up-to-256/512-token showcase limits, not a throughput benchmark.

## 12-request service stability campaign

One continuously loaded server processed:

- 6 text generation requests;
- 3 vision requests;
- 3 extraction requests.

Result:

- requests passed: **12/12**;
- median wall latency: **3,357 ms**;
- maximum wall latency: **15,482 ms**;
- model identity before/after: unchanged;
- allocated CUDA memory delta: **0 bytes on GPU 0, 0 bytes on GPU 1**;
- reserved CUDA memory delta: **+4 MiB on GPU 0, +4 MiB on GPU 1**.

The stable allocated-memory result is the important service-layer signal; PyTorch allocator reservation is reported separately rather than being mislabeled as an active tensor leak.

## Selected smoke observations

Earlier service smoke observations in the same implementation session included:

- exact text response `QWEN3VL_T4X2_OK`: 1,836 ms, 22 input tokens, 11 generated tokens;
- synthetic office vision request: 17,704 ms, 1,592 input tokens, 128 generated tokens;
- simplified invoice structured extraction: 25,772 ms, 3,327 input tokens, 109 generated tokens, JSON/schema PASS.

Do not treat these single observations as statistically representative latency benchmarks.
