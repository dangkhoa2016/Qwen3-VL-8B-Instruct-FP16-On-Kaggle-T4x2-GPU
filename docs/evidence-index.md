# Evidence Index

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](evidence-index.vi.md)

## Evidence classes

| Class | Location | Meaning |
|---|---|---|
| Static definitions | `ground_truth/`, `ASSET_MANIFEST.json` | expected facts, schemas and asset identity |
| Development outputs | `results/` | local/session evidence; intentionally ignored by Git |
| Official evidence index | `benchmarks/official/` | source-controlled contract that points to immutable official evidence |
| Official execution evidence | exact Kaggle notebook/version + GitHub Release assets | reviewed runtime artifacts, manifests and checksums tied to the frozen source SHA |
| Notebook source | `notebooks/kaggle-production-showcase.ipynb` | executable reviewer path before the official run |

CI uses mocks/static verification and must never be described as real T4×2 model evidence. After the official Kaggle execution begins from the frozen commit, evidence publication must not require rewriting that source history.
