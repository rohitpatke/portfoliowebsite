"""Project list and detail pages for both tracks: /academic/ and /professional/."""

from __future__ import annotations

from flask import Blueprint, abort, render_template

from ..services.content import get_content

bp = Blueprint("projects", __name__)

# Only the two track names match; any other first path segment is a 404.
KIND = "<any(academic, professional):kind>"


@bp.get(f"/{KIND}/")
def list_projects(kind: str) -> str:
    """All projects of one track."""
    return render_template("projects/list.html", kind=kind, projects=get_content().by_type(kind))


@bp.get(f"/{KIND}/<slug>/")
def detail(kind: str, slug: str) -> str:
    """Paper layout for academic projects, case-study layout for professional ones."""
    project = get_content().get(kind, slug)
    if project is None:
        abort(404)
    return render_template(f"projects/{kind}.html", project=project)
