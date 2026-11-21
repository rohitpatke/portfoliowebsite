"""Retrieval interface for the future AI features.

FUTURE STUB: nothing calls this yet. The chatbot and JD matcher will depend on the
``Retriever`` protocol, so the strategy can change (send everything, then embeddings
built by scripts/build_index.py) without touching the routes.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from .chunking import Chunk


class Retriever(Protocol):
    """Finds the chunks most relevant to a query."""

    def retrieve(self, query: str, limit: int | None = None) -> list[Chunk]:
        """Return up to ``limit`` chunks, most relevant first."""
        ...


class FullContextRetriever:
    """Returns every chunk. A portfolio is small enough to fit in one prompt.

    Replace with an embedding-based retriever once the content outgrows the model's
    context window or the per-request cost matters.
    """

    def __init__(self, chunks: Sequence[Chunk]) -> None:
        self._chunks = list(chunks)

    def retrieve(self, query: str, limit: int | None = None) -> list[Chunk]:
        """Ignore the query and return all chunks (truncated to ``limit`` if given)."""
        return self._chunks if limit is None else self._chunks[:limit]
