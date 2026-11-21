"""Export the site as static HTML into build/ with Frozen-Flask.

Usage:
    python scripts/freeze.py
    FREEZER_BASE_URL=https://you.github.io/portfolio/ python scripts/freeze.py   # URL prefix

Writes one index.html per page (/, /academic/, /professional/, every project), copies
static files, and adds 404.html and .nojekyll for static hosts.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # allow `python scripts/freeze.py` from the repo root

from flask import render_template  # noqa: E402
from flask_frozen import Freezer  # noqa: E402

from app import create_app  # noqa: E402
from app.models import PROJECT_TYPES  # noqa: E402

app = create_app("production")
freezer = Freezer(app)
content = app.extensions["content"]


@freezer.register_generator
def list_projects() -> Iterator[tuple[str, dict[str, str]]]:
    """Both list pages, even when a track has no projects yet."""
    for kind in PROJECT_TYPES:
        yield "projects.list_projects", {"kind": kind}


@freezer.register_generator
def detail() -> Iterator[tuple[str, dict[str, str]]]:
    """Every project page, including ones not linked from the homepage."""
    for project in content.all():
        yield "projects.detail", {"kind": project.type, "slug": project.slug}


def write_extras(destination: Path) -> None:
    """Add 404.html (GitHub Pages, Netlify and Cloudflare Pages serve it) and .nojekyll."""
    with app.test_request_context(base_url=app.config.get("FREEZER_BASE_URL") or None):
        (destination / "404.html").write_text(render_template("main/404.html"), encoding="utf-8")
    (destination / ".nojekyll").touch()


def main() -> None:
    """Freeze the site and report what was written."""
    freezer.freeze()
    destination = Path(app.config["FREEZER_DESTINATION"])
    write_extras(destination)
    pages = sorted(p.relative_to(destination).as_posix() for p in destination.rglob("*.html"))
    print(f"Froze {len(pages)} pages into {destination}:")
    for page in pages:
        print(f"  {page}")


if __name__ == "__main__":
    main()
