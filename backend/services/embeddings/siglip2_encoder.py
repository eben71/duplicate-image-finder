"""SigLIP-2 image embeddings."""

from __future__ import annotations

from typing import Any, List, Optional

import io

from PIL import Image

try:  # pragma: no cover - optional dependency
    from transformers import AutoModel, AutoProcessor  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    AutoModel = None  # type: ignore[assignment]
    AutoProcessor = None  # type: ignore[assignment]

_DEFAULT_MODEL_NAME = "google/siglip-base-patch16-224"

try:  # pragma: no cover - optional dependency
    import torch  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    torch = None  # type: ignore[assignment]


class SigLIP2Encoder:
    """Wrap a SigLIP (or SigLIP 2) vision encoder."""

    def __init__(
        self,
        model_name: str = _DEFAULT_MODEL_NAME,
        device: Optional[str] = None,
        *,
        processor: Optional[Any] = None,
        model: Optional[Any] = None,
    ) -> None:
        if torch is None and model is None:
            raise RuntimeError("PyTorch is required to load SigLIP models. Install torch>=2.3.0.")
        if AutoModel is None and model is None:
            raise RuntimeError("transformers is required to load SigLIP checkpoints. Install transformers>=4.44.0.")
        if AutoProcessor is None and processor is None:
            raise RuntimeError("transformers is required to load SigLIP checkpoints. Install transformers>=4.44.0.")

        self.model_name = model_name
        if torch is not None and device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device or "cpu"
        self.processor = processor or AutoProcessor.from_pretrained(model_name)
        self.model = model or AutoModel.from_pretrained(model_name)

        if hasattr(self.model, "to"):
            self.model.to(self.device)
        if hasattr(self.model, "eval"):
            self.model.eval()

        config = getattr(self.model, "config", None)
        self.output_dim = getattr(config, "projection_dim", None) or getattr(config, "hidden_size", 768)

    def embed_pil(self, img: Image.Image) -> List[float]:
        if torch is None:
            raise RuntimeError("PyTorch is required to compute embeddings.")

        @torch.no_grad()
        def _forward() -> List[float]:
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
                vector = self.model.get_image_features(**inputs)  # type: ignore[misc]
            else:
                last_hidden = getattr(outputs, "last_hidden_state", None)
                if last_hidden is None:
                    raise RuntimeError("Cannot extract image embeddings from SigLIP model output")
                vector = last_hidden.mean(dim=1)

            vector = torch.nn.functional.normalize(vector, p=2, dim=-1)
            return vector[0].detach().cpu().tolist()

        return _forward()

    def _move_to_device(self, inputs: Any) -> Any:
        if torch is not None and hasattr(inputs, "to"):
            return inputs.to(self.device)

        if isinstance(inputs, dict):
            return {key: self._move_to_device(value) for key, value in inputs.items()}

        return inputs

    def embed_bytes(self, image_bytes: bytes) -> List[float]:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return self.embed_pil(img)

