from __future__ import annotations

from dataclasses import asdict, dataclass
from threading import Lock
from typing import Any

import torch
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration

from .config import Settings


def _normalize_device(value: object) -> object:
    if isinstance(value, torch.device):
        if value.type == "cuda":
            return int(value.index or 0)
        return value.type
    if isinstance(value, str) and value.startswith("cuda:"):
        return int(value.split(":", 1)[1])
    return value


def audit_device_map(model: object) -> dict[str, Any]:
    raw_map = getattr(model, "hf_device_map", None)
    if not isinstance(raw_map, dict) or not raw_map:
        raise RuntimeError("Model is missing a non-empty hf_device_map")

    normalized = {str(k): _normalize_device(v) for k, v in raw_map.items()}
    values = set(normalized.values())
    if "cpu" in values:
        raise RuntimeError("CPU weight offload is forbidden for the baseline")
    if "disk" in values:
        raise RuntimeError("disk weight offload is forbidden for the baseline")

    gpu_ids = sorted(v for v in values if isinstance(v, int))
    if gpu_ids != [0, 1]:
        raise RuntimeError(
            f"Baseline requires weights on both GPU 0 and GPU 1 only; observed {gpu_ids}"
        )

    unsupported = values.difference({0, 1})
    if unsupported:
        raise RuntimeError(f"Unsupported device-map targets: {sorted(map(str, unsupported))}")

    return {
        "gpu_ids": gpu_ids,
        "cpu_weight_offload": False,
        "disk_weight_offload": False,
        "device_map": normalized,
    }


@dataclass(frozen=True, slots=True)
class RuntimeInfo:
    model_id: str
    model_path: str
    architecture: str
    dtype: str
    attention: str
    device_map_strategy: str
    gpu_count: int
    gpu_names: list[str]
    cpu_weight_offload: bool
    disk_weight_offload: bool
    device_map: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ModelRuntime:
    _instance: "ModelRuntime | None" = None
    _load_lock = Lock()

    def __init__(self, model: object, processor: object, info: RuntimeInfo):
        self.model = model
        self.processor = processor
        self.info = info

    @classmethod
    def load(cls, settings: Settings) -> "ModelRuntime":
        with cls._load_lock:
            if cls._instance is not None:
                return cls._instance

            if not torch.cuda.is_available() or torch.cuda.device_count() != 2:
                raise RuntimeError("Exactly two CUDA GPUs are required for the T4x2 baseline")
            gpu_names = [torch.cuda.get_device_name(i) for i in range(2)]
            if any("T4" not in name for name in gpu_names):
                raise RuntimeError(f"Expected Tesla T4 x2, observed: {gpu_names}")
            if not settings.model_path.is_dir():
                raise RuntimeError(f"Attached model path not found: {settings.model_path}")

            processor = AutoProcessor.from_pretrained(
                settings.model_path,
                local_files_only=True,
            )
            model = Qwen3VLForConditionalGeneration.from_pretrained(
                settings.model_path,
                local_files_only=True,
                dtype=torch.float16,
                attn_implementation="sdpa",
                device_map="balanced",
                max_memory={0: "12GiB", 1: "12GiB"},
                low_cpu_mem_usage=True,
            )
            model.eval()
            placement = audit_device_map(model)

            floating_dtypes = {
                p.dtype for p in model.parameters() if getattr(p, "is_floating_point", lambda: False)()
            }
            if floating_dtypes != {torch.float16}:
                raise RuntimeError(f"Expected native FP16 weights only, observed {floating_dtypes}")

            info = RuntimeInfo(
                model_id="Qwen/Qwen3-VL-8B-Instruct",
                model_path=str(settings.model_path),
                architecture=model.__class__.__name__,
                dtype="torch.float16",
                attention="sdpa",
                device_map_strategy="balanced",
                gpu_count=2,
                gpu_names=gpu_names,
                cpu_weight_offload=placement["cpu_weight_offload"],
                disk_weight_offload=placement["disk_weight_offload"],
                device_map=placement["device_map"],
            )
            cls._instance = cls(model=model, processor=processor, info=info)
            return cls._instance

    @classmethod
    def reset_for_tests(cls) -> None:
        cls._instance = None
