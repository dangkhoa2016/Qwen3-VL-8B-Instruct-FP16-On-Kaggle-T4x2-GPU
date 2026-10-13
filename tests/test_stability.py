from qwen3vl_t4x2.stability import build_request_plan, summarize_stability


def test_request_plan_mixes_all_three_inference_endpoints():
    plan = build_request_plan(12)
    endpoints = [item["endpoint"] for item in plan]
    assert len(plan) == 12
    assert "/v1/generate" in endpoints
    assert "/v1/vision" in endpoints
    assert "/v1/extract" in endpoints
    assert endpoints.count("/v1/generate") >= endpoints.count("/v1/vision")


def test_stability_summary_reports_runtime_and_allocated_memory_delta():
    records = [
        {"success": True, "endpoint": "/v1/generate", "latency_ms": 10},
        {"success": True, "endpoint": "/v1/vision", "latency_ms": 20},
        {"success": True, "endpoint": "/v1/extract", "latency_ms": 30},
    ]
    before = {"gpu": [{"index": 0, "allocated_bytes": 100, "reserved_bytes": 200}, {"index": 1, "allocated_bytes": 300, "reserved_bytes": 400}]}
    after = {"gpu": [{"index": 0, "allocated_bytes": 110, "reserved_bytes": 250}, {"index": 1, "allocated_bytes": 305, "reserved_bytes": 450}]}

    summary = summarize_stability(records, before, after)

    assert summary["requests_total"] == 3
    assert summary["requests_pass"] == 3
    assert summary["requests_failed"] == 0
    assert summary["allocated_delta_bytes"] == {"0": 10, "1": 5}
    assert summary["reserved_delta_bytes"] == {"0": 50, "1": 50}


def test_stability_summary_keeps_failed_request_visible():
    records = [
        {"success": True, "endpoint": "/v1/generate", "latency_ms": 10},
        {"success": False, "endpoint": "/v1/vision", "latency_ms": 20},
    ]
    metrics = {"gpu": []}
    summary = summarize_stability(records, metrics, metrics)
    assert summary["requests_pass"] == 1
    assert summary["requests_failed"] == 1
    assert summary["service_stability_gate"] == "FAIL"
