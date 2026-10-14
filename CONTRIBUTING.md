# Contributing

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](CONTRIBUTING.vi.md)

Contributions should be small, reviewable and evidence-preserving.

## Development rules

- Add or update tests before behavior changes.
- Preserve the strict FP16/T4×2/no-offload baseline unless the change explicitly introduces a separately documented mode.
- Keep runtime success separate from semantic quality evaluation.
- Never describe mocked GitHub Actions output as real Kaggle GPU evidence.
- Keep English/Vietnamese documentation pairs synchronized.
- Do not commit API keys, Kaggle/Hugging Face credentials or tunnel secrets.

## Local verification

Run `pytest -q`, `python -m compileall -q src scripts`, asset verification, notebook verification, repository audit and secret scan before proposing a merge.
