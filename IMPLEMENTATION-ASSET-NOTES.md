# Implementation Asset Notes

## Primary benchmark capability groups

- General Vision Understanding: 3 deterministic synthetic cases + 2 real-world public-domain/CC0 cases.
- OCR + Document Understanding: transit notice, warehouse summary, invoice understanding, receipt understanding.
- Generic Structured Extraction: invoice, receipt, business card, service request form.
- Tables / Charts / Visual Reasoning: 2 tables + 3 charts.
- Multilingual & Mixed-Context Vision: 3 English/Vietnamese cases.

An additional real-world urban-market case is marked `general_vision_optional`.

## Validation classes

- Exact structured fields: programmatic comparison is appropriate.
- Numeric table/chart answers: programmatic exact checks are appropriate.
- Free-form vision: use required-fact checks plus a short reviewer note.
- Real-world scene descriptions: qualitative reviewer check; do not claim exact semantic PASS solely from HTTP status.

## External image preparation

After unpacking on the connected machine:

```bash
bash scripts/fetch_public_domain_vision_assets.sh .
python scripts/verify_asset_pack.py .
```

The static verifier intentionally permits missing assets whose case has `requires_fetch=true`.
