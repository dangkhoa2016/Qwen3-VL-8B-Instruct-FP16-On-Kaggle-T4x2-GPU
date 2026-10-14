# Implementation Asset Notes

## Release capability groups

- General Vision Understanding: 4 cases, including AI-generated photorealistic office and waterfront market scenes plus controlled spatial/relationship scenes.
- OCR + Document Understanding: 4 cases, including photorealistic invoice/receipt understanding.
- Generic Structured Extraction: 4 core schemas plus one Vietnamese extraction case in the multilingual group.
- Tables / Charts / Visual Reasoning: 4 curated reasoning cases.
- Multilingual & Mixed-Context Vision: 3 English/Vietnamese cases, including a photorealistic bilingual workshop poster.

The release catalog contains **19 runnable cases** and every required image is committed locally. There is no runtime image download/fetch step.

## Asset classes

- `examples/realistic/`: six AI-generated photorealistic JPEG assets created for this project, resized to 1024×768.
- remaining `examples/`: programmatically generated controlled documents, charts, tables and visual scenes.

## Validation classes

- Structured extraction: JSON parse + requested-schema validation + expected-field comparison.
- Numeric table/chart answers: reviewer-visible exact values/arithmetic.
- Free-form vision/document answers: manual expected-fact review; HTTP 200 alone is never a semantic PASS.

Run `python scripts/verify_asset_pack.py .` to verify all committed image hashes and case references.
