from __future__ import annotations

import json
from typing import Any

from jsonschema import validate

_PRIMITIVES = {
    "string": {"type": "string"},
    "number": {"type": "number"},
    "integer": {"type": "integer"},
    "boolean": {"type": "boolean"},
}


def _normalize(node: Any) -> dict[str, Any]:
    if isinstance(node, str):
        if node not in _PRIMITIVES:
            raise ValueError(f"Unsupported schema type: {node}")
        return dict(_PRIMITIVES[node])

    if isinstance(node, list):
        if len(node) != 1:
            raise ValueError("Array schema must contain exactly one item schema")
        return {"type": "array", "items": _normalize(node[0])}

    if isinstance(node, dict):
        properties = {str(key): _normalize(value) for key, value in node.items()}
        return {
            "type": "object",
            "properties": properties,
            "required": list(properties),
            "additionalProperties": False,
        }

    raise ValueError(f"Unsupported schema node: {type(node).__name__}")


def normalize_schema(spec: object) -> dict[str, Any]:
    if not isinstance(spec, dict) or not spec:
        raise ValueError("Extraction schema must be a non-empty object")
    return _normalize(spec)


def validate_extracted(value: object, normalized: dict[str, Any]) -> None:
    validate(instance=value, schema=normalized)


def build_extraction_instruction(spec: object) -> str:
    normalized = normalize_schema(spec)
    return (
        "Extract the visible information from the image according to the schema below. "
        "Do not invent values that are not visible. Return JSON only, with no markdown fences, "
        "commentary, or additional keys.\nSchema:\n"
        + json.dumps(normalized, ensure_ascii=False, indent=2)
    )
