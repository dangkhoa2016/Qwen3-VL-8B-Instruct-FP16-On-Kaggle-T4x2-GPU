from types import SimpleNamespace

import pytest

from qwen3vl_t4x2.runtime import audit_device_map


def _model(device_map):
    return SimpleNamespace(hf_device_map=device_map)


def test_audit_accepts_weights_on_both_gpus_only():
    result = audit_device_map(
        _model({"model.visual": 0, "model.language_model.layers.0": 0, "model.language_model.layers.1": 1, "lm_head": 1})
    )
    assert result["gpu_ids"] == [0, 1]
    assert result["cpu_weight_offload"] is False
    assert result["disk_weight_offload"] is False


def test_audit_rejects_cpu_weight_offload():
    with pytest.raises(RuntimeError, match="CPU weight offload"):
        audit_device_map(_model({"model.visual": 0, "lm_head": "cpu"}))


def test_audit_rejects_disk_weight_offload():
    with pytest.raises(RuntimeError, match="disk weight offload"):
        audit_device_map(_model({"model.visual": 0, "lm_head": "disk"}))


def test_audit_requires_both_gpu_zero_and_one():
    with pytest.raises(RuntimeError, match="both GPU 0 and GPU 1"):
        audit_device_map(_model({"model.visual": 0, "lm_head": 0}))


def test_audit_rejects_missing_accelerate_device_map():
    with pytest.raises(RuntimeError, match="hf_device_map"):
        audit_device_map(SimpleNamespace())
