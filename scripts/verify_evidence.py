#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qwen3vl_t4x2.evidence import summarize_records


def main() -> None:
    results_path = ROOT / "results" / "showcase-results.jsonl"
    summary_path = ROOT / "results" / "showcase-summary.json"
    if not results_path.is_file() or not summary_path.is_file():
        raise SystemExit("EVIDENCE_VERIFY=FAIL missing evidence files")

    records = [json.loads(line) for line in results_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    stored = json.loads(summary_path.read_text(encoding="utf-8"))
    recomputed = summarize_records(records)
    keys = [
        "showcase_cases_total",
        "showcase_runtime_pass",
        "showcase_runtime_fail",
        "semantic_auto_evaluated",
        "semantic_auto_pass",
        "structured_cases_total",
        "structured_parse_rate",
        "structured_schema_valid_rate",
    ]
    mismatches = [key for key in keys if stored.get(key) != recomputed.get(key)]
    if mismatches:
        raise SystemExit(f"EVIDENCE_VERIFY=FAIL summary mismatch: {mismatches}")

    model = stored.get("model_runtime", {})
    if model.get("dtype") != "torch.float16":
        raise SystemExit("EVIDENCE_VERIFY=FAIL dtype is not torch.float16")
    if model.get("gpu_count") != 2:
        raise SystemExit("EVIDENCE_VERIFY=FAIL gpu_count is not 2")
    if model.get("cpu_weight_offload") or model.get("disk_weight_offload"):
        raise SystemExit("EVIDENCE_VERIFY=FAIL offload detected")

    print(f"EVIDENCE_VERIFY=PASS cases={len(records)} runtime_pass={recomputed['showcase_runtime_pass']}")


if __name__ == "__main__":
    main()
