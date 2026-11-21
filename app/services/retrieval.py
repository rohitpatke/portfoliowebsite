"""FUTURE: retrieval interface for the AI features. Nothing calls this yet."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from .chunking import Chunk


class Retriever(Protocol):
    def retrieve(self, query: str, limit: int | None = None) -> list[Chunk]:
        ...


class FullContextRetriever:
    """Returns every chunk; a portfolio fits in one prompt."""

    def __init__(self, chunks: Sequence[Chunk]) -> None:
        self._chunks = list(chunks)

    def retrieve(self, query: str, limit: int | None = None) -> list[Chunk]:
        return self._chunks if limit is None else self._chunks[:limit]
