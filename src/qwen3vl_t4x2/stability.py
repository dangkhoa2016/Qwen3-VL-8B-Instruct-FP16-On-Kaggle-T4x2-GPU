from __future__ import annotations

from collections import Counter
from statistics import median
from typing import Any


def build_request_plan(requests: int) -> list[dict[str, str]]:
    if requests < 3:
        raise ValueError("Stability run requires at least 3 requests")
    cycle = [
        {"endpoint": "/v1/generate", "case_id": "text-smoke"},
        {"endpoint": "/v1/generate", "case_id": "text-vi"},
        {"endpoint": "/v1/vision", "case_id": "vision-office"},
        {"endpoint": "/v1/extract", "case_id": "invoice-minimal"},
    ]
    return [dict(cycle[i % len(cycle)]) for i in range(requests)]


def _gpu_values(metrics: dict[str, Any], key: str) -> dict[str, int]:
    return {
        str(item["index"]): int(item.get(key, 0))
        for item in metrics.get("gpu", [])
    }


def summarize_stability(records: list[dict[str, Any]], before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    total = len(records)
    passed = sum(1 for record in records if record.get("success") is True)
    failed = total - passed
    latencies = [int(record.get("latency_ms", 0)) for record in records]
    by_endpoint = Counter(str(record.get("endpoint")) for record in records)

    before_alloc = _gpu_values(before, "allocated_bytes")
    after_alloc = _gpu_values(after, "allocated_bytes")
    before_reserved = _gpu_values(before, "reserved_bytes")
    after_reserved = _gpu_values(after, "reserved_bytes")
    gpu_ids = sorted(set(before_alloc) | set(after_alloc) | set(before_reserved) | set(after_reserved))

    allocated_delta = {gpu: after_alloc.get(gpu, 0) - before_alloc.get(gpu, 0) for gpu in gpu_ids}
    reserved_delta = {gpu: after_reserved.get(gpu, 0) - before_reserved.get(gpu, 0) for gpu in gpu_ids}

    return {
        "requests_total": total,
        "requests_pass": passed,
        "requests_failed": failed,
        "by_endpoint": dict(by_endpoint),
        "latency_ms": {
            "median": int(round(median(latencies))) if latencies else 0,
            "max": max(latencies) if latencies else 0,
        },
        "allocated_delta_bytes": allocated_delta,
        "reserved_delta_bytes": reserved_delta,
        "service_stability_gate": "PASS" if total > 0 and failed == 0 else "FAIL",
    }
