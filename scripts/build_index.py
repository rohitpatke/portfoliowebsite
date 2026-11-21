"""FUTURE STUB: build an embedding index of project chunks. Prints the chunk count."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import CONTENT_DIR  # noqa: E402
from app.services.chunking import project_to_chunks  # noqa: E402
from app.services.content import ContentRepository  # noqa: E402


def main() -> int:
    content = ContentRepository(CONTENT_DIR)
    chunks = [chunk for project in content.all() for chunk in project_to_chunks(project)]
    print(f"{len(chunks)} chunks from {len(content.all())} projects would be indexed.")
    print("build_index: not implemented (see app/ai/README.md).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
