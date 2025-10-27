"""Duplicate filtering service exports."""

from backend.services.dedupe.pipeline import DedupePipeline
from backend.services.dedupe.pdq_filter import PDQFilter

__all__ = ["DedupePipeline", "PDQFilter"]
