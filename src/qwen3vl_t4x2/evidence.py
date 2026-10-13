from __future__ import annotations

from typing import Any
import re
import unicodedata


_DASH_TRANSLATION = str.maketrans({"–": "-", "—": "-", "−": "-", "‑": "-"})


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).translate(_DASH_TRANSLATION)
    return re.sub(r"\s+", " ", normalized).strip()


def _subset_mismatches(expected: Any, actual: Any, path: str = "") -> list[str]:
    mismatches: list[str] = []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{path or '<root>'}: expected object, got {type(actual).__name__}"]
        for key, value in expected.items():
            child = f"{path}.{key}" if path else str(key)
            if key not in actual:
                mismatches.append(f"{child}: missing")
            else:
                mismatches.extend(_subset_mismatches(value, actual[key], child))
        return mismatches

    if isinstance(expected, list):
        if not isinstance(actual, list):
            return [f"{path}: expected list, got {type(actual).__name__}"]
        if expected != actual:
            return [f"{path}: expected {expected!r}, got {actual!r}"]
        return []

    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if abs(float(expected) - float(actual)) > 1e-6:
            mismatches.append(f"{path}: expected {expected!r}, got {actual!r}")
        return mismatches

    if isinstance(expected, str) and isinstance(actual, str):
        if _normalize_text(expected) != _normalize_text(actual):
            mismatches.append(f"{path}: expected {expected!r}, got {actual!r}")
        return mismatches

    if expected != actual:
        mismatches.append(f"{path}: expected {expected!r}, got {actual!r}")
    return mismatches


def evaluate_case(case: dict[str, Any], status_code: int, response: dict[str, Any]) -> dict[str, Any]:
    runtime_success = 200 <= status_code < 300 and response.get("success", True) is not False
    endpoint = str(case.get("endpoint", ""))

    if not runtime_success:
        semantic = {"mode": "not_evaluated", "pass": None}
    elif endpoint == "/v1/extract":
        expected = case.get("expected", {})
        actual = response.get("data")
        mismatches = _subset_mismatches(expected, actual)
        semantic = {
            "mode": "expected_subset",
            "pass": not mismatches,
            "mismatches": mismatches,
        }
    else:
        semantic = {"mode": "manual", "pass": None}

    return {
        "case_id": case.get("case_id"),
        "group": case.get("group"),
        "endpoint": endpoint,
        "runtime_success": runtime_success,
        "semantic_validation": semantic,
        "response": response,
    }


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(records)
    runtime_pass = sum(1 for r in records if r.get("runtime_success") is True)
    auto = [
        r for r in records
        if r.get("semantic_validation", {}).get("mode") not in {"manual", "not_evaluated"}
    ]
    auto_pass = sum(1 for r in auto if r.get("semantic_validation", {}).get("pass") is True)

    structured = [r for r in records if r.get("endpoint") == "/v1/extract"]
    parse_pass = sum(
        1 for r in structured
        if r.get("response", {}).get("meta", {}).get("json_parse") is True
    )
    schema_pass = sum(
        1 for r in structured
        if r.get("response", {}).get("meta", {}).get("schema_valid") is True
    )
    denom = len(structured) or 1

    return {
        "showcase_cases_total": total,
        "showcase_runtime_pass": runtime_pass,
        "showcase_runtime_fail": total - runtime_pass,
        "semantic_auto_evaluated": len(auto),
        "semantic_auto_pass": auto_pass,
        "structured_cases_total": len(structured),
        "structured_parse_rate": parse_pass / denom if structured else 0.0,
        "structured_schema_valid_rate": schema_pass / denom if structured else 0.0,
    }
