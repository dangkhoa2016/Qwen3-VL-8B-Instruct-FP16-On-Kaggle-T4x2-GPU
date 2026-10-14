# Benchmarks and Evidence

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](benchmarks.vi.md)


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

## Photorealistic 19-case showcase campaign

The current self-contained release catalog contains 19 runnable cases across five capability groups:

| Capability | Cases |
|---|---:|
| General vision | 4 |
| Structured extraction | 4 |
| OCR/document understanding | 4 |
| Tables/charts | 4 |
| Multilingual | 3 |
| **Total** | **19** |

One multilingual case also uses `/v1/extract`, so there are **5 structured endpoint cases** in the campaign. Six reviewer-facing inputs are AI-generated photorealistic assets (office, waterfront produce market, invoice, receipt, business card and bilingual workshop poster); no third-party web photograph is required.

Final development-session result for the current asset/catalog/prompt set:

- runtime success: **19/19**;
- JSON parse rate across 5 structured endpoint cases: **100%**;
- schema validation rate: **100%**;
- expected-field semantic checks: **5/5 PASS** after deliberately narrow text normalization (`NFKC`, whitespace collapse, typographic-dash equivalence only);
- free-form cases: **14/14 manually reviewed for the expected facts** in this development session; free-form answers are still not auto-labeled semantic PASS by the evidence engine.

Per-case wall latency for this campaign (not cumulative server metrics): **13,822 ms median**, **5,356 ms minimum**, **32,115 ms maximum**. This is a deep showcase campaign, not a throughput benchmark.

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


## Development-case curation note

During development review, a close-line crossing-point question exposed a genuine reasoning inconsistency: the model correctly read `A=61` and `B=63` at W3 but still described A as greater. The release showcase therefore does not auto-present that crossing-point prompt as a quality PASS. The retained line-chart case tests exact labeled-value reading plus arithmetic differences instead. This curation is documented rather than hidden as evaluator tolerance. A grouped-bar exact-difference case was also removed from the default release catalog after repeated inference showed inconsistent category/sign reasoning even after the chart was made numerically explicit; the asset remains available, but that failed reasoning probe is not represented as a release quality PASS.
