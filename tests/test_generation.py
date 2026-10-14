from io import BytesIO
from types import SimpleNamespace

import pytest
import torch
from PIL import Image

from qwen3vl_t4x2.config import Settings
from qwen3vl_t4x2.generation import (
    GenerationResult,
    decode_uploaded_image,
    generate_text,
)


class FakeBatch(dict):
    def to(self, device):
        self["moved_to"] = str(device)
        return self


class FakeProcessor:
    def __init__(self):
        self.messages = None

    def apply_chat_template(self, messages, **kwargs):
        self.messages = messages
        return FakeBatch({"input_ids": torch.tensor([[10, 20, 30]])})

    def batch_decode(self, token_ids, **kwargs):
        return ["decoded response"]


class FakeModel:
    device = torch.device("cpu")

    def generate(self, **kwargs):
        return torch.tensor([[10, 20, 30, 40, 50]])


@pytest.fixture
def runtime():
    return SimpleNamespace(model=FakeModel(), processor=FakeProcessor())


def test_generate_text_uses_chat_template_and_counts_tokens(runtime):
    result = generate_text(runtime, "hello", max_new_tokens=32, temperature=0.0)
    assert isinstance(result, GenerationResult)
    assert result.output == "decoded response"
    assert result.input_tokens == 3
    assert result.generated_tokens == 2
    assert result.latency_ms >= 0
    content = runtime.processor.messages[0]["content"]
    assert content == [{"type": "text", "text": "hello"}]


def test_decode_uploaded_image_accepts_png_and_normalizes_rgb(monkeypatch):
    settings = Settings.from_env()
    image = Image.new("RGBA", (64, 32), (255, 0, 0, 128))
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    decoded = decode_uploaded_image(buffer.getvalue(), "image/png", settings)

    assert decoded.mode == "RGB"
    assert decoded.size == (64, 32)


def test_decode_uploaded_image_rejects_unsupported_mime():
    settings = Settings.from_env()
    with pytest.raises(ValueError, match="Unsupported image content type"):
        decode_uploaded_image(b"not-an-image", "image/gif", settings)


def test_decode_uploaded_image_rejects_large_dimensions():
    settings = Settings.from_env()
    image = Image.new("RGB", (settings.max_image_dimension + 1, 10), "white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    with pytest.raises(ValueError, match="dimensions"):
        decode_uploaded_image(buffer.getvalue(), "image/png", settings)


def test_generate_vision_places_image_before_prompt(runtime):
    from qwen3vl_t4x2.generation import generate_vision

    image = Image.new("RGB", (16, 16), "white")
    result = generate_vision(runtime, image, "What is visible?", max_new_tokens=16, temperature=0.0)

    assert result.output == "decoded response"
    content = runtime.processor.messages[0]["content"]
    assert content[0]["type"] == "image"
    assert content[0]["image"] is image
    assert content[1] == {"type": "text", "text": "What is visible?"}


def test_generate_extraction_uses_schema_instruction(runtime):
    from qwen3vl_t4x2.generation import generate_extraction

    image = Image.new("RGB", (16, 16), "white")
    result = generate_extraction(
        runtime,
        image,
        {"invoice_number": "string", "total": "number"},
        max_new_tokens=64,
    )

    assert result.output == "decoded response"
    prompt = runtime.processor.messages[0]["content"][1]["text"]
    assert "Return JSON only" in prompt
    assert '"invoice_number"' in prompt
