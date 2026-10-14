from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import json
from time import perf_counter
from typing import Any

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from jsonschema import ValidationError
from pydantic import BaseModel

from .config import Settings
from .generation import (
    decode_uploaded_image,
    generate_extraction,
    generate_text,
    generate_vision,
)
from .metrics import MetricsStore
from .runtime import ModelRuntime
from .schemas import normalize_schema, validate_extracted
from .security import requires_public_auth, verify_bearer_token


class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int | None = None
    temperature: float = 0.0


def _error(status_code: int, code: str, message: str, *, meta: dict[str, Any] | None = None) -> JSONResponse:
    payload: dict[str, Any] = {
        "success": False,
        "error": {"code": code, "message": message},
    }
    if meta is not None:
        payload["meta"] = meta
    return JSONResponse(status_code=status_code, content=payload)


def _validated_generation_args(settings: Settings, prompt: str, max_new_tokens: int | None, temperature: float) -> tuple[int, float]:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must not be empty")
    if len(prompt) > settings.max_prompt_chars:
        raise ValueError("Prompt exceeds the configured character limit")
    tokens = settings.default_max_new_tokens if max_new_tokens is None else int(max_new_tokens)
    if tokens < 1 or tokens > settings.max_new_tokens_limit:
        raise ValueError("max_new_tokens exceeds the configured limit")
    if temperature < 0:
        raise ValueError("temperature must be non-negative")
    return tokens, float(temperature)


def create_app(settings: Settings, runtime: Any | None = None) -> FastAPI:
    metrics = MetricsStore()
    inference_lock = asyncio.Lock()
    state: dict[str, Any] = {"runtime": runtime}

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        if state["runtime"] is None:
            state["runtime"] = ModelRuntime.load(settings)
        yield

    app = FastAPI(title="Qwen3-VL-8B-Instruct T4x2 API", version="0.1.0", lifespan=lifespan)

    @app.middleware("http")
    async def collect_metrics(request, call_next):
        started = perf_counter()
        metrics.begin(request.url.path)
        if requires_public_auth(request.headers.get("host"), settings):
            try:
                verify_bearer_token(request.headers.get("authorization"), settings)
            except PermissionError as exc:
                code = str(exc)
                message = "Bearer API key is required" if code == "AUTH_REQUIRED" else "Bearer API key is invalid"
                response = _error(401, code, message)
                metrics.end(status_code=response.status_code, latency_ms=int(round((perf_counter() - started) * 1000)))
                return response
        try:
            response = await call_next(request)
        except Exception:
            metrics.end(status_code=500, latency_ms=int(round((perf_counter() - started) * 1000)))
            raise
        metrics.end(status_code=response.status_code, latency_ms=int(round((perf_counter() - started) * 1000)))
        return response

    def require_runtime() -> Any:
        current = state["runtime"]
        if current is None:
            raise RuntimeError("MODEL_NOT_READY")
        return current

    @app.get("/health")
    async def health():
        ready = state["runtime"] is not None
        if not ready:
            return JSONResponse(status_code=503, content={"status": "starting", "model_loaded": False, "ready": False})
        return {"status": "ok", "model_loaded": True, "ready": True}

    @app.get("/v1/model")
    async def model_info():
        try:
            return require_runtime().info.as_dict()
        except RuntimeError:
            return _error(503, "MODEL_NOT_READY", "Model is not ready")

    @app.post("/v1/generate")
    async def generate(request: GenerateRequest):
        try:
            max_new_tokens, temperature = _validated_generation_args(settings, request.prompt, request.max_new_tokens, request.temperature)
            async with inference_lock:
                result = generate_text(require_runtime(), request.prompt, max_new_tokens=max_new_tokens, temperature=temperature)
            return {"success": True, "output": result.output, "meta": result.meta()}
        except ValueError as exc:
            return _error(400, "INVALID_REQUEST", str(exc))
        except RuntimeError as exc:
            if str(exc) == "MODEL_NOT_READY":
                return _error(503, "MODEL_NOT_READY", "Model is not ready")
            return _error(500, "INFERENCE_FAILED", str(exc))

    @app.post("/v1/vision")
    async def vision(image: UploadFile = File(...), prompt: str = Form(...), max_new_tokens: int | None = Form(None), temperature: float = Form(0.0)):
        try:
            max_new_tokens, temperature = _validated_generation_args(settings, prompt, max_new_tokens, temperature)
            decoded = decode_uploaded_image(await image.read(), image.content_type, settings)
            async with inference_lock:
                result = generate_vision(require_runtime(), decoded, prompt, max_new_tokens=max_new_tokens, temperature=temperature)
            return {"success": True, "output": result.output, "meta": result.meta()}
        except ValueError as exc:
            return _error(400, "INVALID_IMAGE" if "image" in str(exc).lower() else "INVALID_REQUEST", str(exc))
        except RuntimeError as exc:
            if str(exc) == "MODEL_NOT_READY":
                return _error(503, "MODEL_NOT_READY", "Model is not ready")
            return _error(500, "INFERENCE_FAILED", str(exc))

    @app.post("/v1/extract")
    async def extract(image: UploadFile = File(...), extraction_schema: str = Form(..., alias="schema"), max_new_tokens: int | None = Form(None)):
        started = perf_counter()
        try:
            if len(extraction_schema.encode("utf-8")) > settings.max_schema_bytes:
                raise ValueError("Schema exceeds the configured byte limit")
            try:
                compact_schema = json.loads(extraction_schema)
            except json.JSONDecodeError as exc:
                return _error(400, "INVALID_SCHEMA", f"Schema is not valid JSON: {exc.msg}")
            normalized = normalize_schema(compact_schema)
            decoded = decode_uploaded_image(await image.read(), image.content_type, settings)
            tokens = settings.default_max_new_tokens if max_new_tokens is None else int(max_new_tokens)
            if tokens < 1 or tokens > settings.max_new_tokens_limit:
                raise ValueError("max_new_tokens exceeds the configured limit")
            async with inference_lock:
                result = generate_extraction(require_runtime(), decoded, compact_schema, max_new_tokens=tokens)
            try:
                parsed = json.loads(result.output)
                validate_extracted(parsed, normalized)
            except (json.JSONDecodeError, ValidationError):
                return _error(422, "STRUCTURED_OUTPUT_INVALID", "Model output could not be validated against the requested schema.", meta={"latency_ms": result.latency_ms})
            meta = result.meta()
            meta.update({"json_parse": True, "schema_valid": True})
            return {"success": True, "data": parsed, "meta": meta}
        except ValueError as exc:
            message = str(exc)
            code = "INVALID_SCHEMA" if "schema" in message.lower() else "INVALID_IMAGE" if "image" in message.lower() else "INVALID_REQUEST"
            return _error(400, code, message)
        except RuntimeError as exc:
            if str(exc) == "MODEL_NOT_READY":
                return _error(503, "MODEL_NOT_READY", "Model is not ready")
            return _error(500, "INFERENCE_FAILED", str(exc), meta={"latency_ms": int(round((perf_counter() - started) * 1000))})

    @app.get("/v1/metrics")
    async def runtime_metrics():
        return metrics.snapshot()

    return app
