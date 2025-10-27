from __future__ import annotations

import io

from PIL import Image

from backend.services.dedupe.pdq_filter import PDQFilter


def test_pdq_hash_returns_hex_string() -> None:
    img = Image.new("RGB", (16, 16), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    filter_ = PDQFilter(method="auto")
    hash_hex, quality, method = filter_.compute_hash(buffer.getvalue())

    assert isinstance(hash_hex, str)
    assert hash_hex
    assert method in {"pdq", "phash"}
    assert quality is None or isinstance(quality, int)


def test_hamming_distance_is_zero_for_identical_hashes() -> None:
    hash_hex = "ff0f"
    assert PDQFilter.hamming_distance(hash_hex, hash_hex) == 0
