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
        "scripts/start_server.py",
        "/v1/model",
        "scripts/run_showcase.py",
        "run_stability.py",
        "FINAL_SHOWCASE_RUNTIME=PASS",
        "ENABLE_CLOUDFLARE_TUNNEL",
    ]
    missing = [token for token in required if token not in source]
    if missing:
        raise SystemExit(f"NOTEBOOK_VERIFY=FAIL missing markers: {missing}")
    for index, cell in enumerate(cells):
        if cell.get("cell_type") == "code":
            compile("".join(cell.get("source", [])), f"{path}::cell{index}", "exec")
    run_showcase_calls = sum("scripts/run_showcase.py" in "".join(cell.get("source", [])) for cell in cells)
    if run_showcase_calls != 1:
        raise SystemExit(f"NOTEBOOK_VERIFY=FAIL expected exactly one showcase execution, got {run_showcase_calls}")
    print(f"NOTEBOOK_VERIFY=PASS cells={len(cells)} showcase_runs={run_showcase_calls}")


if __name__ == "__main__":
    main()
