"""Duplicate detection pipeline combining PDQ and vector similarity."""

from __future__ import annotations

from typing import Any, Dict, List

from backend.services.dedupe.pdq_filter import PDQFilter
from backend.services.embeddings.siglip2_encoder import SigLIP2Encoder
from backend.services.vector.pgvector_store import VectorStore

PDQ_MAX_HAMMING = 8
TOPK = 50


class DedupePipeline:
    """Run PDQ filtering before vector similarity search."""

    def __init__(self, vector_store: VectorStore, encoder: SigLIP2Encoder):
        self.pdq = PDQFilter(method="auto")
        self.vs = vector_store
        self.encoder = encoder

    def find_candidates(self, image_bytes: bytes, user_id: int) -> List[Dict[str, Any]]:
        target_hash, _, method = self.pdq.compute_hash(image_bytes)

        query_matches = self.vs.fetch_pdq_candidates(user_id=user_id, limit=200)

        pdq_hits: List[Dict[str, Any]] = []
        for record in query_matches:
            stored_hash = record.get("pdq_hash")
            if not stored_hash:
                continue

            distance = PDQFilter.hamming_distance(target_hash, stored_hash)
            if distance <= PDQ_MAX_HAMMING:
                enriched = dict(record)
                enriched["pdq_distance"] = distance
                enriched["pdq_method"] = method
                pdq_hits.append(enriched)

        if pdq_hits:
            return sorted(pdq_hits, key=lambda item: item["pdq_distance"])  # type: ignore[index]

        embedding = self.encoder.embed_bytes(image_bytes)
        neighbors = self.vs.search(embedding=embedding, user_id=user_id, top_k=TOPK)
        return neighbors

