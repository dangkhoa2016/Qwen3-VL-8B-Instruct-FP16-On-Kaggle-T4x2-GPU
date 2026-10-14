# Official Benchmark Evidence Index

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

This directory is the source-controlled index and contract for official benchmark evidence. It intentionally does **not** store mutable post-run result dumps that would require rewriting the source commit after an official Kaggle execution.

For an official campaign, the immutable evidence authority is the executed Kaggle notebook/version plus the matching GitHub Release assets and checksums. Every official evidence set must identify the exact frozen source commit it executed.

Development/session outputs remain under `results/` and are ignored by Git. Mocked CI output or exploratory artifacts must never be presented as real T4×2 inference evidence.

Once the official Kaggle execution starts from the frozen source commit, **do not rewrite Git history after the official Kaggle execution starts**. Review and publish the resulting evidence externally without changing that proven source SHA.
