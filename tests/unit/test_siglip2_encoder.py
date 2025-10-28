from __future__ import annotations

import io
from types import SimpleNamespace

import pytest

pytest.importorskip("torch")
import torch
from PIL import Image

from backend.services.embeddings.siglip2_encoder import SigLIP2Encoder


class DummyBatch:
    def __init__(self) -> None:
        self.data = {"pixel_values": torch.ones((1, 3, 4, 4))}

    def to(self, device: str) -> DummyBatch:
        return self


class DummyProcessor:
    def __call__(self, *, images: Image.Image, return_tensors: str) -> DummyBatch:
        assert return_tensors == "pt"
        return DummyBatch()


class DummyOutputs:
    def __init__(self) -> None:
        self.image_embeds = torch.ones((1, 3), dtype=torch.float32)


class DummyModel:
    def __init__(self) -> None:
        self.config = SimpleNamespace(projection_dim=3)

    def to(self, device: str) -> DummyModel:
        return self

    def eval(self) -> DummyModel:
        return self

    def __call__(self, **kwargs):
        return DummyOutputs()


def test_siglip2_encoder_with_injected_stubs() -> None:
    encoder = SigLIP2Encoder(processor=DummyProcessor(), model=DummyModel())

    img = Image.new("RGB", (8, 8), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    vector = encoder.embed_bytes(buffer.getvalue())

    assert len(vector) == encoder.output_dim == 3
    norm = sum(value * value for value in vector)
    assert norm == pytest.approx(1.0, rel=1e-6)
