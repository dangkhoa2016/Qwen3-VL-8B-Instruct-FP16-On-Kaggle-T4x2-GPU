from qwen3vl_t4x2.evidence import evaluate_case, summarize_records


def test_extract_case_passes_when_expected_fields_match_subset():
    case = {
        "case_id": "invoice-01",
        "endpoint": "/v1/extract",
        "expected": {"invoice_number": "INV-1", "total": 12.5},
    }
    response = {
        "success": True,
        "data": {"invoice_number": "INV-1", "total": 12.5, "items": []},
        "meta": {"json_parse": True, "schema_valid": True, "latency_ms": 10},
    }

    record = evaluate_case(case, 200, response)

    assert record["runtime_success"] is True
    assert record["semantic_validation"]["mode"] == "expected_subset"
    assert record["semantic_validation"]["pass"] is True
    assert record["semantic_validation"]["mismatches"] == []


def test_extract_case_reports_mismatch_without_overriding_runtime_success():
    case = {
        "case_id": "invoice-01",
        "endpoint": "/v1/extract",
        "expected": {"total": 12.5},
    }
    response = {
        "success": True,
        "data": {"total": 99.0},
        "meta": {"json_parse": True, "schema_valid": True},
    }

    record = evaluate_case(case, 200, response)

    assert record["runtime_success"] is True
    assert record["semantic_validation"]["pass"] is False
    assert "total" in record["semantic_validation"]["mismatches"][0]


def test_vision_case_is_manual_not_auto_pass():
    case = {
        "case_id": "vision-01",
        "endpoint": "/v1/vision",
        "expected": {"must_notice": ["desk", "mug"]},
    }
    response = {"success": True, "output": "A desk and mug are visible.", "meta": {}}

    record = evaluate_case(case, 200, response)

    assert record["runtime_success"] is True
    assert record["semantic_validation"] == {"mode": "manual", "pass": None}


def test_summary_keeps_runtime_and_semantic_counts_separate():
    records = [
        {"runtime_success": True, "endpoint": "/v1/extract", "semantic_validation": {"mode": "expected_subset", "pass": True}, "response": {"meta": {"json_parse": True, "schema_valid": True}}},
        {"runtime_success": True, "endpoint": "/v1/vision", "semantic_validation": {"mode": "manual", "pass": None}, "response": {"meta": {}}},
        {"runtime_success": False, "endpoint": "/v1/extract", "semantic_validation": {"mode": "not_evaluated", "pass": None}, "response": {}},
    ]

    summary = summarize_records(records)

    assert summary["showcase_cases_total"] == 3
    assert summary["showcase_runtime_pass"] == 2
    assert summary["semantic_auto_evaluated"] == 1
    assert summary["semantic_auto_pass"] == 1
    assert summary["structured_parse_rate"] == 0.5
    assert summary["structured_schema_valid_rate"] == 0.5


def test_expected_subset_treats_typographic_dash_variants_as_equivalent():
    case = {
        "case_id": "form-01",
        "endpoint": "/v1/extract",
        "expected": {"window": "2026-10-14, 09:00–12:00"},
    }
    response = {
        "success": True,
        "data": {"window": "2026-10-14, 09:00-12:00"},
        "meta": {"json_parse": True, "schema_valid": True},
    }

    record = evaluate_case(case, 200, response)

    assert record["semantic_validation"]["pass"] is True
    assert record["semantic_validation"]["mismatches"] == []
