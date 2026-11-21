"""ContentRepository: the only code that reads ``content/``, once at startup."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import frontmatter
import markdown
import yaml
from flask import current_app
from pydantic import ValidationError

from ..models import COMPUTED_FIELDS, PROJECT_TYPES, Project

MARKDOWN_EXTENSIONS = ["extra", "sane_lists"]
SITE_REQUIRED_KEYS = (
    "name", "initials", "tagline", "headline", "status", "email", "linkedin",
    "hero", "services", "experience", "organizations", "skill_aliases",
)


class ContentError(RuntimeError):
    """A content file is missing or invalid."""


def render_markdown(text: str) -> str:
    return markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS, output_format="html")


def load_project(path: Path) -> Project:
    try:
        post = frontmatter.load(path)
    except (yaml.YAMLError, UnicodeDecodeError) as error:
        raise ContentError(f"{path}: could not parse frontmatter: {error}") from error

    clashes = COMPUTED_FIELDS & post.metadata.keys()
    if clashes:
        raise ContentError(f"{path}: remove {', '.join(sorted(clashes))}; they are set automatically")

    data = {
        **post.metadata,
        "slug": path.stem,
        "type": path.parent.name,
        "body_html": render_markdown(post.content),
    }
    try:
        return Project.model_validate(data)
    except ValidationError as error:
        raise ContentError(f"{path}: invalid project\n{error}") from error


def load_site(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ContentError(f"{path} not found")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ContentError(f"{path}: expected a mapping at the top level")
    missing = [key for key in SITE_REQUIRED_KEYS if key not in data]
    if missing:
        raise ContentError(f"{path}: missing keys: {', '.join(missing)}")
    aliases = data["skill_aliases"]
    if not isinstance(aliases, dict) or not all(isinstance(v, list) for v in aliases.values()):
        raise ContentError(f"{path}: skill_aliases must map each skill to a list of terms")
    return data


class ContentRepository:
    def __init__(self, content_dir: Path) -> None:
        self.content_dir = content_dir
        self.site: dict[str, Any] = load_site(content_dir / "site.yaml")
        self._aliases = {
            skill.lower(): [str(term).lower() for term in terms]
            for skill, terms in self.site["skill_aliases"].items()
        }
        self._projects = self._load_projects()

    def _load_projects(self) -> list[Project]:
        projects = [
            load_project(path)
            for kind in PROJECT_TYPES
            for path in sorted((self.content_dir / kind).glob("*.md"))
        ]
        projects.sort(key=lambda p: p.ends, reverse=True)  # newest first...
        projects.sort(key=lambda p: p.order)  # ...within each `order` value (sort is stable)
        return projects

    def all(self) -> list[Project]:
        return list(self._projects)

    def by_type(self, kind: str) -> list[Project]:
        return [p for p in self._projects if p.type == kind]

    def featured(self) -> list[Project]:
        return [p for p in self._projects if p.featured]

    def get(self, kind: str, slug: str) -> Project | None:
        return next((p for p in self._projects if p.type == kind and p.slug == slug), None)

    def skill_terms(self, skill: str) -> list[str]:
        terms = [skill.lower(), *self._aliases.get(skill.lower(), [])]
        return list(dict.fromkeys(terms))

    def match_records(self, url_for_project: Callable[[Project], str]) -> list[dict[str, Any]]:
        """Per-project data for recruiter mode, embedded in the page as JSON."""
        return [
            {
                "title": project.title,
                "type": project.type,
                "label": project.type_label,
                "url": url_for_project(project),
                "evidence": project.summary,
                "skills": [
                    {"name": skill, "terms": self.skill_terms(skill)} for skill in project.skills
                ],
            }
            for project in self._projects
        ]


def get_content() -> ContentRepository:
    return current_app.extensions["content"]
