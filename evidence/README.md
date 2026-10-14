# Evidence Policy

Session-generated evidence is written under `results/` and is intentionally ignored by Git. This avoids committing stale or machine-specific outputs accidentally.

Only reviewed evidence from an official Kaggle T4 x2 execution should be promoted into a versioned benchmark/evidence artifact for a public release.

CI/mock tests may produce labels such as `UNIT_TEST=PASS`, `API_CONTRACT=PASS`, and `STATIC_VALIDATION=PASS`. They must never be presented as real GPU evidence.

Actual Kaggle runs may establish runtime claims such as native FP16 inference, T4 x2 placement, no-offload behavior, REST service stability, and showcase case results.
