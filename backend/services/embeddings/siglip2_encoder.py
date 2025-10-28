"""SigLIP-2 image embeddings."""

from __future__ import annotations

import io
from typing import Any, cast

from PIL import Image

try:  # pragma: no cover - optional dependency
    from transformers import AutoModel as HF_AutoModel  # type: ignore
    from transformers import AutoProcessor as HF_AutoProcessor
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    HF_AutoModel = None  # type: ignore[assignment]
    HF_AutoProcessor = None  # type: ignore[assignment]

TRANSFORMERS_AUTO_MODEL: Any | None = cast(Any, HF_AutoModel)
TRANSFORMERS_AUTO_PROCESSOR: Any | None = cast(Any, HF_AutoProcessor)

_DEFAULT_MODEL_NAME = "google/siglip-base-patch16-224"

try:  # pragma: no cover - optional dependency
    import torch as _torch  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    _torch = None  # type: ignore[assignment]

torch = cast(Any, _torch)


class SigLIP2Encoder:
    """Wrap a SigLIP (or SigLIP 2) vision encoder."""

    def __init__(
        self,
        model_name: str = _DEFAULT_MODEL_NAME,
        device: str | None = None,
        *,
        processor: Any | None = None,
        model: Any | None = None,
    ) -> None:
        if torch is None and model is None:
            raise RuntimeError("PyTorch is required to load SigLIP models. Install torch>=2.3.0.")
        if TRANSFORMERS_AUTO_MODEL is None and model is None:
            raise RuntimeError(
                "transformers is required to load SigLIP checkpoints. Install transformers>=4.44.0."
            )
        if TRANSFORMERS_AUTO_PROCESSOR is None and processor is None:
            raise RuntimeError(
                "transformers is required to load SigLIP checkpoints. Install transformers>=4.44.0."
            )

        self.model_name = model_name
        if torch is not None and device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device or "cpu"
        if processor is None:
            assert TRANSFORMERS_AUTO_PROCESSOR is not None
            resolved_processor = TRANSFORMERS_AUTO_PROCESSOR.from_pretrained(model_name)
        else:
            resolved_processor = processor

        if model is None:
            assert TRANSFORMERS_AUTO_MODEL is not None
            resolved_model = TRANSFORMERS_AUTO_MODEL.from_pretrained(model_name)
        else:
            resolved_model = model

        self.processor = resolved_processor
        self.model = resolved_model

        if hasattr(self.model, "to"):
            self.model.to(self.device)
        if hasattr(self.model, "eval"):
            self.model.eval()

        config = getattr(self.model, "config", None)
        self.output_dim = getattr(config, "projection_dim", None) or getattr(
            config, "hidden_size", 768
        )

    def embed_pil(self, img: Image.Image) -> list[float]:
        if torch is None:
            raise RuntimeError("PyTorch is required to compute embeddings.")

        def _forward() -> list[float]:
            batch = self.processor(images=img, return_tensors="pt")
            batch = self._move_to_device(batch)

            if isinstance(batch, dict):
                inputs: Any = batch
            elif hasattr(batch, "data") and isinstance(batch.data, dict):  # BatchEncoding
                inputs = dict(batch.data)
            else:
                inputs = batch

            outputs = self.model(**inputs) if isinstance(inputs, dict) else self.model(inputs)

            if hasattr(outputs, "image_embeds"):
                vector = outputs.image_embeds
            elif hasattr(self.model, "get_image_features"):
                vector = cast(Any, self.model).get_image_features(**inputs)
            else:
                last_hidden = getattr(outputs, "last_hidden_state", None)
                if last_hidden is None:
                    raise RuntimeError("Cannot extract image embeddings from SigLIP model output")
                vector = last_hidden.mean(dim=1)

            vector = torch.nn.functional.normalize(vector, p=2, dim=-1)
            return vector[0].detach().cpu().tolist()

        with torch.no_grad():
            return _forward()

    def _move_to_device(self, inputs: Any) -> Any:
        if torch is not None and hasattr(inputs, "to"):
            return inputs.to(self.device)

        if isinstance(inputs, dict):
            return {key: self._move_to_device(value) for key, value in inputs.items()}

        return inputs

    def embed_bytes(self, image_bytes: bytes) -> list[float]:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return self.embed_pil(img)
