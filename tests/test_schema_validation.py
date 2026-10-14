import json

import pytest
from jsonschema import ValidationError

from qwen3vl_t4x2.schemas import (
    build_extraction_instruction,
    normalize_schema,
    validate_extracted,
)


def test_normalize_nested_compact_schema():
    compact = {
        "invoice_number": "string",
        "total": "number",
        "items": [{"name": "string", "quantity": "number"}],
    }
    normalized = normalize_schema(compact)
    assert normalized["type"] == "object"
    assert normalized["additionalProperties"] is False
    assert normalized["required"] == ["invoice_number", "total", "items"]
    assert normalized["properties"]["items"]["type"] == "array"
    assert normalized["properties"]["items"]["items"]["type"] == "object"


def test_invalid_compact_type_is_rejected():
    with pytest.raises(ValueError, match="Unsupported schema type"):
        normalize_schema({"total": "decimal"})


def test_empty_array_schema_is_rejected():
    with pytest.raises(ValueError, match="exactly one item schema"):
        normalize_schema({"items": []})


def test_validate_extracted_enforces_required_and_no_extra_fields():
    schema = normalize_schema({"name": "string", "total": "number"})
    validate_extracted({"name": "Acme", "total": 12.5}, schema)
    with pytest.raises(ValidationError):
        validate_extracted({"name": "Acme"}, schema)
    with pytest.raises(ValidationError):
        validate_extracted({"name": "Acme", "total": 12.5, "extra": 1}, schema)


def test_instruction_contains_normalized_schema_and_json_only_rule():
    instruction = build_extraction_instruction({"name": "string", "count": "integer"})
    assert "Return JSON only" in instruction
    assert '"additionalProperties": false' in instruction
    assert '"count"' in instruction
    json.loads(instruction.split("Schema:\n", 1)[1])
