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

from qwen3vl_t4x2.stability import build_request_plan, summarize_stability


def request_once(client: httpx.Client, item: dict[str, str]) -> tuple[bool, int, dict]:
    endpoint = item["endpoint"]
    started = perf_counter()
    if endpoint == "/v1/generate":
        prompt = "Reply with exactly: STABILITY_OK" if item["case_id"] == "text-smoke" else "Trả lời đúng một từ: ỔN"
        response = client.post(endpoint, json={"prompt": prompt, "max_new_tokens": 24, "temperature": 0.0})
    elif endpoint == "/v1/vision":
        asset = ROOT / "examples/vision/vision-synthetic-office-rich.png"
        with asset.open("rb") as handle:
            response = client.post(
                endpoint,
                files={"image": (asset.name, handle, "image/png")},
                data={"prompt": "Name the main workspace objects concisely.", "max_new_tokens": "64", "temperature": "0"},
            )
    elif endpoint == "/v1/extract":
        asset = ROOT / "examples/invoices/invoice-01-northstar.png"
        schema = {"invoice_number": "string", "total": "number"}
        with asset.open("rb") as handle:
            response = client.post(
                endpoint,
                files={"image": (asset.name, handle, "image/png")},
                data={"schema": json.dumps(schema, separators=(",", ":")), "max_new_tokens": "128"},
            )
    else:
        raise ValueError(f"Unsupported endpoint in stability plan: {endpoint}")

    wall_ms = int(round((perf_counter() - started) * 1000))
    try:
        body = response.json()
    except ValueError:
        body = {"success": False, "raw": response.text[:500]}
    success = response.status_code == 200 and body.get("success", True) is not False
    return success, wall_ms, body


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--requests", type=int, default=12)
    parser.add_argument("--output", default=str(ROOT / "results" / "stability-summary.json"))
    args = parser.parse_args()

    plan = build_request_plan(args.requests)
    records = []
    with httpx.Client(base_url=args.base_url, timeout=180.0) as client:
        before = client.get("/v1/metrics").json()
        model_before = client.get("/v1/model").json()
        for index, item in enumerate(plan, 1):
            success, wall_ms, body = request_once(client, item)
            record = {
                "index": index,
                "endpoint": item["endpoint"],
                "case_id": item["case_id"],
                "success": success,
                "latency_ms": wall_ms,
                "response_meta": body.get("meta", {}),
            }
            records.append(record)
            print(f"STABILITY_REQUEST={index}/{len(plan)} ENDPOINT={item['endpoint']} PASS={success} WALL_MS={wall_ms}", flush=True)
        model_after = client.get("/v1/model").json()
        after = client.get("/v1/metrics").json()

    summary = summarize_stability(records, before, after)
    summary.update({
        "server_model_identity_stable": model_before == model_after,
        "model_before": model_before,
        "model_after": model_after,
        "metrics_before": before,
        "metrics_after": after,
        "records": records,
    })
    if not summary["server_model_identity_stable"]:
        summary["service_stability_gate"] = "FAIL"

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k not in {"model_before", "model_after", "metrics_before", "metrics_after", "records"}}, indent=2))
    if summary["service_stability_gate"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
