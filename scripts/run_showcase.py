#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from time import perf_counter

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qwen3vl_t4x2.evidence import evaluate_case, summarize_records


def select_cases(cases, case_ids, groups, max_cases, include_external):
    selected = []
    for case in cases:
        if case.get("requires_fetch") and not include_external:
            continue
        if case_ids and case.get("case_id") not in case_ids:
            continue
        if groups and case.get("group") not in groups:
            continue
        selected.append(case)
        if max_cases and len(selected) >= max_cases:
            break
    return selected


def execute_case(client: httpx.Client, case: dict) -> tuple[int, dict, int]:
    asset = ROOT / case["asset"]
    if not asset.is_file():
        return 0, {"success": False, "error": {"code": "ASSET_MISSING", "message": str(asset)}}, 0

    started = perf_counter()
    with asset.open("rb") as handle:
        files = {"image": (asset.name, handle, "image/png" if asset.suffix.lower() == ".png" else "image/jpeg")}
        if case["endpoint"] == "/v1/vision":
            data = {
                "prompt": case["prompt"],
                "max_new_tokens": "256",
                "temperature": "0",
            }
        elif case["endpoint"] == "/v1/extract":
            data = {
                "schema": json.dumps(case["schema"], ensure_ascii=False, separators=(",", ":")),
                "max_new_tokens": "512",
            }
        else:
            return 0, {"success": False, "error": {"code": "UNSUPPORTED_ENDPOINT", "message": case["endpoint"]}}, 0
        response = client.post(case["endpoint"], files=files, data=data)
    wall_ms = int(round((perf_counter() - started) * 1000))
    try:
        body = response.json()
    except ValueError:
        body = {"success": False, "error": {"code": "NON_JSON_RESPONSE", "message": response.text[:1000]}}
    return response.status_code, body, wall_ms


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--group", action="append", default=[])
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--include-external", action="store_true")
    parser.add_argument("--output-dir", default=str(ROOT / "results"))
    args = parser.parse_args()

    cases = json.loads((ROOT / "ground_truth" / "cases.json").read_text(encoding="utf-8"))
    selected = select_cases(cases, set(args.case_id), set(args.group), args.max_cases, args.include_external)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "showcase-results.jsonl"
    summary_path = output_dir / "showcase-summary.json"

    records = []
    with httpx.Client(base_url=args.base_url, timeout=240.0) as client, jsonl_path.open("w", encoding="utf-8") as out:
        health = client.get("/health"); health.raise_for_status()
        model = client.get("/v1/model"); model.raise_for_status()
        for case in selected:
            status_code, response, wall_ms = execute_case(client, case)
            record = evaluate_case(case, status_code, response)
            record.update({
                "asset": case.get("asset"),
                "http_status": status_code,
                "wall_latency_ms": wall_ms,
                "request": {"prompt": case.get("prompt"), "schema": case.get("schema")},
                "expected": case.get("expected"),
            })
            records.append(record)
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            out.flush()
            verdict = record["semantic_validation"].get("pass")
            print(f"CASE={case['case_id']} HTTP={status_code} RUNTIME={record['runtime_success']} SEMANTIC={verdict}", flush=True)
        metrics = client.get("/v1/metrics").json()

    summary = summarize_records(records)
    summary.update({
        "server_health": health.json(),
        "model_runtime": model.json(),
        "metrics": metrics,
        "selected_case_ids": [c["case_id"] for c in selected],
        "results_jsonl": str(jsonl_path),
    })
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
