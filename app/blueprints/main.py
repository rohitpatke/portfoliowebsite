from __future__ import annotations

from flask import Blueprint, render_template, url_for

from ..models import Project
from ..services.content import get_content

bp = Blueprint("main", __name__)


def project_url(project: Project) -> str:
    return url_for("projects.detail", kind=project.type, slug=project.slug)


@bp.get("/")
def index() -> str:
    content = get_content()
    return render_template(
        "main/index.html",
        featured=content.featured(),
        publications=content.by_type("academic"),
        match_data=content.match_records(project_url),
    )
