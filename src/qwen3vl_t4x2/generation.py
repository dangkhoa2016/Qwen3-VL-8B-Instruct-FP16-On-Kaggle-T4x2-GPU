from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from time import perf_counter
from typing import Any

import torch
from PIL import Image, UnidentifiedImageError

from .config import Settings
from .schemas import build_extraction_instruction


@dataclass(frozen=True, slots=True)
class GenerationResult:
    output: str
    input_tokens: int
    generated_tokens: int
    latency_ms: int

    def meta(self) -> dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "generated_tokens": self.generated_tokens,
            "latency_ms": self.latency_ms,
        }


def decode_uploaded_image(data: bytes, content_type: str | None, settings: Settings) -> Image.Image:
    allowed = {"image/jpeg", "image/png", "image/webp"}
    if content_type not in allowed:
        raise ValueError(f"Unsupported image content type: {content_type}")
    if not data or len(data) > settings.max_upload_bytes:
        raise ValueError("Image upload size is invalid or exceeds the configured limit")
    try:
        image = Image.open(BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Uploaded file is not a valid image") from exc
    if image.width > settings.max_image_dimension or image.height > settings.max_image_dimension:
        raise ValueError("Image dimensions exceed the configured limit")
    return image.convert("RGB")


def _generate(runtime: Any, messages: list[dict[str, Any]], *, max_new_tokens: int, temperature: float) -> GenerationResult:
    inputs = runtime.processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )
    model_device = getattr(runtime.model, "device", torch.device("cuda:0"))
    inputs = inputs.to(model_device)
    input_tokens = int(inputs["input_ids"].shape[1])
    kwargs: dict[str, Any] = {"max_new_tokens": max_new_tokens, "do_sample": temperature > 0}
    if temperature > 0:
        kwargs["temperature"] = temperature
    started = perf_counter()
    with torch.inference_mode():
        generated = runtime.model.generate(**inputs, **kwargs)
    latency_ms = int(round((perf_counter() - started) * 1000))
    trimmed = generated[:, input_tokens:]
    output = runtime.processor.batch_decode(
        trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0].strip()
    return GenerationResult(
        output=output,
        input_tokens=input_tokens,
        generated_tokens=int(trimmed.shape[1]),
        latency_ms=latency_ms,
    )


def generate_text(runtime: Any, prompt: str, *, max_new_tokens: int, temperature: float) -> GenerationResult:
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    return _generate(runtime, messages, max_new_tokens=max_new_tokens, temperature=temperature)


def generate_vision(runtime: Any, image: Image.Image, prompt: str, *, max_new_tokens: int, temperature: float) -> GenerationResult:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt},
            ],
        }
    ]
    return _generate(runtime, messages, max_new_tokens=max_new_tokens, temperature=temperature)


def generate_extraction(runtime: Any, image: Image.Image, schema: object, *, max_new_tokens: int) -> GenerationResult:
    prompt = build_extraction_instruction(schema)
    return generate_vision(
        runtime,
        image,
        prompt,
        max_new_tokens=max_new_tokens,
        temperature=0.0,
    )
