# Chỉ mục Evidence

> 🌐 Language / Ngôn ngữ: [English](evidence-index.md) | **Tiếng Việt**

## Các loại evidence

| Loại | Vị trí | Ý nghĩa |
|---|---|---|
| Static definitions | `ground_truth/`, `ASSET_MANIFEST.json` | expected facts, schemas và asset identity |
| Development outputs | `results/` | evidence theo session; được Git ignore |
| Official evidence index | `benchmarks/official/` | source-controlled contract trỏ tới immutable official evidence |
| Official execution evidence | exact Kaggle notebook/version + GitHub Release assets | runtime artifacts, manifests và checksums đã review, gắn với frozen source SHA |
| Notebook source | `notebooks/kaggle-production-showcase.ipynb` | luồng executable cho reviewer trước official run |

CI dùng mock/static verification và không được mô tả là evidence inference T4×2 thật. Sau khi official Kaggle execution bắt đầu từ frozen commit, việc publish evidence không được yêu cầu rewrite source history đó.
