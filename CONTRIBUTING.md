# Contributing

Contributions should preserve the repository's evidence integrity rules: do not label mocked/CI results as Kaggle GPU evidence, do not silently change dtype/offload behavior, and keep runtime success separate from semantic validation.

For changes, add or update tests first where behavior changes, run `pytest -q`, run asset/notebook static verification, and describe any measured GPU evidence separately from unit-test results.

Never commit API keys, Hugging Face/Kaggle credentials or public-tunnel secrets.
