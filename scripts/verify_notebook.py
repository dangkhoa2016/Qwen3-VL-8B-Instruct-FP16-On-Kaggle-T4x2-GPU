#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_notebook.py <notebook.ipynb>")
    path = Path(sys.argv[1])
    nb = json.loads(path.read_text(encoding="utf-8"))
    if nb.get("nbformat") != 4:
        raise SystemExit("NOTEBOOK_VERIFY=FAIL nbformat must be 4")
    cells = nb.get("cells", [])
    if not cells:
        raise SystemExit("NOTEBOOK_VERIFY=FAIL notebook has no cells")
    source = "\n".join("".join(cell.get("source", [])) for cell in cells)
    required = [
        "Attach the Kaggle Model",
        "GPU T4 ×2",
        "git clone",
        "REPO_REF",
        "git checkout",
        "scripts/start_server.py",
        "/health",
        "/v1/model",
        "/v1/generate",
        "/v1/vision",
        "/v1/extract",
        "scripts/run_showcase.py",
        "run_stability.py",
        "FINAL_SHOWCASE_RUNTIME=PASS",
        "ENABLE_CLOUDFLARE_TUNNEL",
        "default: False",
        "General Visual Understanding",
        "Spatial & Relationship Reasoning",
        "OCR & Document Understanding",
        "Structured JSON Extraction",
        "Tables & Visual Data Reasoning",
        "Charts & Numerical Reasoning",
        "Vietnamese & Multilingual",
        "REST API Examples",
        "Performance & Stability",
        "Final Scorecard",
        "Latency",
        "Semantic",
    ]
    missing = [token for token in required if token not in source]
    if missing:
        raise SystemExit(f"NOTEBOOK_VERIFY=FAIL missing markers: {missing}")

    markdown_cells = [cell for cell in cells if cell.get("cell_type") == "markdown"]
    bilingual_missing = []
    bilingual_heading_style = []
    for index, cell in enumerate(cells):
        if cell.get("cell_type") != "markdown":
            continue
        text = "".join(cell.get("source", []))
        if "English:" not in text or "Tiếng Việt:" not in text:
            bilingual_missing.append(index)
        if "### English" in text or "## English" in text or "### Tiếng Việt" in text or "## Tiếng Việt" in text:
            bilingual_heading_style.append(index)
    if bilingual_missing:
        raise SystemExit(
            "NOTEBOOK_VERIFY=FAIL markdown cells missing literal English:/Tiếng Việt: blocks: "
            + ",".join(map(str, bilingual_missing))
        )
    if bilingual_heading_style:
        raise SystemExit(
            "NOTEBOOK_VERIFY=FAIL language labels must be content labels, not markdown headings: "
            + ",".join(map(str, bilingual_heading_style))
        )

    if "Before you run / Trước khi chạy" not in source:
        raise SystemExit("NOTEBOOK_VERIFY=FAIL missing bilingual before-you-run guidance")
    expected_evidence_count = source.count("Expected evidence / Kết quả cần thấy")
    if expected_evidence_count < 10:
        raise SystemExit(
            f"NOTEBOOK_VERIFY=FAIL expected at least 10 bilingual evidence guidance blocks, got {expected_evidence_count}"
        )
    for index, cell in enumerate(cells):
        if cell.get("cell_type") == "code":
            compile("".join(cell.get("source", [])), f"{path}::cell{index}", "exec")
    run_showcase_calls = sum(
        "scripts/run_showcase.py" in "".join(cell.get("source", []))
        for cell in cells
        if cell.get("cell_type") == "code"
    )
    if run_showcase_calls != 1:
        raise SystemExit(f"NOTEBOOK_VERIFY=FAIL expected exactly one showcase execution, got {run_showcase_calls}")
    print(f"NOTEBOOK_VERIFY=PASS cells={len(cells)} showcase_runs={run_showcase_calls}")


if __name__ == "__main__":
    main()
