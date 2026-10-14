import json
from io import BytesIO
from types import SimpleNamespace

from fastapi.testclient import TestClient
from PIL import Image

from qwen3vl_t4x2.config import Settings
from qwen3vl_t4x2.generation import GenerationResult


class FakeInfo:
    def as_dict(self):
        return {
            "model_id": "Qwen/Qwen3-VL-8B-Instruct",
            "dtype": "torch.float16",
            "gpu_count": 2,
            "gpu_names": ["Tesla T4", "Tesla T4"],
            "cpu_weight_offload": False,
            "disk_weight_offload": False,
        }


class FakeRuntime:
    info = FakeInfo()


def _png_bytes():
    buf = BytesIO()
    Image.new("RGB", (32, 24), "white").save(buf, format="PNG")
    return buf.getvalue()


def test_health_and_model_contract(monkeypatch):
    from qwen3vl_t4x2.api import create_app

    client = TestClient(create_app(Settings.from_env(), runtime=FakeRuntime()))
    health = client.get("/health")
    model = client.get("/v1/model")

    assert health.status_code == 200
    assert health.json() == {"status": "ok", "model_loaded": True, "ready": True}
    assert model.status_code == 200
    assert model.json()["dtype"] == "torch.float16"
    assert model.json()["gpu_count"] == 2


def test_generate_contract(monkeypatch):
    import qwen3vl_t4x2.api as api_module

    monkeypatch.setattr(
        api_module,
        "generate_text",
        lambda *args, **kwargs: GenerationResult("answer", 4, 2, 15),
    )
    client = TestClient(api_module.create_app(Settings.from_env(), runtime=FakeRuntime()))
    response = client.post("/v1/generate", json={"prompt": "hello", "max_new_tokens": 64, "temperature": 0.0})

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "output": "answer",
        "meta": {"input_tokens": 4, "generated_tokens": 2, "latency_ms": 15},
    }


def test_vision_accepts_multipart_upload(monkeypatch):
    import qwen3vl_t4x2.api as api_module

    monkeypatch.setattr(
        api_module,
        "generate_vision",
        lambda *args, **kwargs: GenerationResult("vision answer", 10, 3, 21),
    )
    client = TestClient(api_module.create_app(Settings.from_env(), runtime=FakeRuntime()))
    response = client.post(
        "/v1/vision",
        files={"image": ("sample.png", _png_bytes(), "image/png")},
        data={"prompt": "describe", "max_new_tokens": "32", "temperature": "0"},
    )

    assert response.status_code == 200
    assert response.json()["output"] == "vision answer"


def test_extract_parses_and_validates_json(monkeypatch):
    import qwen3vl_t4x2.api as api_module

    monkeypatch.setattr(
        api_module,
        "generate_extraction",
        lambda *args, **kwargs: GenerationResult('{"name":"Acme","total":12.5}', 20, 8, 31),
    )
    client = TestClient(api_module.create_app(Settings.from_env(), runtime=FakeRuntime()))
    response = client.post(
        "/v1/extract",
        files={"image": ("invoice.png", _png_bytes(), "image/png")},
        data={"schema": json.dumps({"name": "string", "total": "number"}), "max_new_tokens": "128"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"] == {"name": "Acme", "total": 12.5}
    assert body["meta"]["schema_valid"] is True


def test_extract_returns_structured_output_invalid_for_bad_json(monkeypatch):
    import qwen3vl_t4x2.api as api_module

    monkeypatch.setattr(
        api_module,
        "generate_extraction",
        lambda *args, **kwargs: GenerationResult("not json", 20, 2, 9),
    )
    client = TestClient(api_module.create_app(Settings.from_env(), runtime=FakeRuntime()))
    response = client.post(
        "/v1/extract",
        files={"image": ("invoice.png", _png_bytes(), "image/png")},
        data={"schema": json.dumps({"name": "string"})},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "STRUCTURED_OUTPUT_INVALID"


def test_metrics_endpoint_exists():
    from qwen3vl_t4x2.api import create_app

    client = TestClient(create_app(Settings.from_env(), runtime=FakeRuntime()))
    response = client.get("/v1/metrics")
    assert response.status_code == 200
    assert response.json()["requests_total"] >= 1


def test_public_host_requires_bearer_when_tunnel_enabled(monkeypatch):
    from qwen3vl_t4x2.api import create_app

    monkeypatch.setenv("ENABLE_CLOUDFLARE_TUNNEL", "true")
    monkeypatch.setenv("QWEN3VL_API_KEY", "secret-key")
    settings = Settings.from_env()
    client = TestClient(
        create_app(settings, runtime=FakeRuntime()),
        base_url="https://demo.trycloudflare.com",
    )

    missing = client.get("/health")
    wrong = client.get("/health", headers={"Authorization": "Bearer wrong"})
    valid = client.get("/health", headers={"Authorization": "Bearer secret-key"})

    assert missing.status_code == 401
    assert missing.json()["error"]["code"] == "AUTH_REQUIRED"
    assert wrong.status_code == 401
    assert wrong.json()["error"]["code"] == "AUTH_INVALID"
    assert valid.status_code == 200
