"""PDQ perceptual hashing helpers."""

from __future__ import annotations

from typing import Optional, Tuple

import io
import logging

from PIL import Image

try:  # pragma: no cover - optional dependency
    import pdqhash  # type: ignore

    HAS_PDQ = True
except Exception:  # pragma: no cover - optional dependency
    pdqhash = None  # type: ignore
    HAS_PDQ = False

import imagehash

_warned_pdq_missing = False

logger = logging.getLogger(__name__)


class PDQFilter:
    """Compute perceptual hashes with an optional PDQ backend."""

    def __init__(self, method: str = "auto") -> None:
        self.method = method

    def _pdq_hash(self, pil_img: Image.Image) -> Tuple[str, int]:
        """Return ``(hash_hex, quality)`` using a PDQ implementation if available."""

        if not HAS_PDQ or pdqhash is None:  # pragma: no cover - guarded by caller
            raise RuntimeError("PDQ library not available")

        # Try a few common Python bindings. Saving to bytes keeps APIs uniform.
        buffer = io.BytesIO()
        pil_img.save(buffer, format="JPEG")
        payload = buffer.getvalue()

        # facebookresearch/pdqhash python bindings expose ``compute``
        if hasattr(pdqhash, "compute"):
            result = pdqhash.compute(payload)  # type: ignore[call-arg]
            if isinstance(result, tuple) and len(result) >= 2:
                hexhash, quality = result[0], result[1]
            else:  # pragma: no cover - depends on binding implementation
                hexhash, quality = str(result), 100
            return str(hexhash), int(quality)

        # Some forks expose ``pdqhash`` returning (quality, hash)
        if hasattr(pdqhash, "pdqhash"):
            quality, hexhash = pdqhash.pdqhash(payload)  # type: ignore[attr-defined]
            return str(hexhash), int(quality)

        raise RuntimeError("Unsupported PDQ binding")

    def _phash(self, pil_img: Image.Image) -> str:
        return str(imagehash.phash(pil_img))

    def compute_hash(self, image_bytes: bytes) -> Tuple[str, Optional[int], str]:
        """Return ``(hash_hex, quality_or_none, backend_used)``."""

        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert("RGB")

        wants_pdq = self.method == "pdq" or (self.method == "auto" and HAS_PDQ)
        if wants_pdq:
            try:
                hash_hex, quality = self._pdq_hash(img)
                return hash_hex, quality, "pdq"
            except Exception as exc:  # pragma: no cover - depends on optional dep
                logger.warning(
                    "PDQ hashing failed (%s); falling back to pHash for duplicate filtering.",
                    exc,
                )

        global _warned_pdq_missing
        if (self.method in {"auto", "pdq"}) and not HAS_PDQ and not _warned_pdq_missing:
            logger.warning(
                "pdqhash bindings are unavailable; PDQFilter will fall back to imagehash.pHash until installed.",
            )
            _warned_pdq_missing = True

        if self.method == "pdq" and not HAS_PDQ:
            logger.warning(
                "PDQ hashing requested but pdqhash bindings are unavailable; using pHash fallback.",
            )

        hash_hex = self._phash(img)
        return hash_hex, None, "phash"

    @staticmethod
    def hamming_distance(h1: str, h2: str) -> int:
        """Return the Hamming distance between two hexadecimal hashes."""

        return bin(int(h1, 16) ^ int(h2, 16)).count("1")

