"""FUTURE STUB: build an embedding index of project chunks for the AI features.

Today it only shows what would be indexed. The README roadmap describes the plan:
embed each chunk from app/services/chunking.py, save the vectors next to the chunk ids,
and load them in an embedding-based Retriever (app/services/retrieval.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # allow `python scripts/build_index.py` from the repo root

from app.config import Config  # noqa: E402
from app.services.chunking import project_to_chunks  # noqa: E402
from app.services.content import ContentRepository  # noqa: E402


def main() -> int:
    """Print the chunk count, then report that indexing is not implemented."""
    content = ContentRepository(Config.CONTENT_DIR)
    chunks = [chunk for project in content.all() for chunk in project_to_chunks(project)]
    print(f"{len(chunks)} chunks from {len(content.all())} projects would be indexed.")
    print("build_index: not implemented (see README, 'Roadmap: AI features').")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
