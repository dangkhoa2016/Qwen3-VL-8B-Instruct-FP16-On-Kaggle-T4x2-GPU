# Benchmark Methodology

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](benchmark-methodology.vi.md)

The project separates **runtime success**, **structured semantic validation**, and **manual free-form review**. HTTP 200 alone is never treated as a quality pass.

## Measurement rules

- Record per-case wall latency from the client side.
- Record model identity, dtype, GPU count and offload state with the campaign.
- For `/v1/extract`, require JSON parsing and JSON-Schema validation before semantic checks.
- Compare only fields explicitly declared in ground truth; do not silently repair model output.
- Free-form vision/OCR reasoning is reviewed manually against expected facts.
- Report campaign median/min/max from that campaign's records, not cumulative server metrics.

## Development campaign

The current reviewed development campaign contains 19 release-candidate cases across general vision, structured extraction, OCR/document understanding, tables/charts and multilingual understanding. It remains development evidence until an official Kaggle run from the frozen source SHA is reviewed and published as the authoritative evidence set.
