# Evidence Workspace

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

This directory documents the evidence contract. Development/session outputs belong in `results/` and are intentionally ignored by Git. `benchmarks/official/` is the source-controlled index for official evidence; the executed Kaggle notebook/version and matching GitHub Release assets are the immutable runtime evidence authority.

Official evidence must be reviewed against the exact frozen source commit. CI/static verification is supporting evidence, not real model-inference evidence, and post-run publication must not rewrite the proven source SHA.
