"""Content validation: every project file must load, and site.yaml must stay consistent."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from app.config import CONTENT_DIR
from app.models import PROJECT_TYPES, Project
from app.services.chunking import project_to_chunks
from app.services.content import ContentError, ContentRepository, load_project

PROJECT_FILES = sorted(path for kind in PROJECT_TYPES for path in (CONTENT_DIR / kind).glob("*.md"))


@pytest.fixture(scope="module")
def content() -> ContentRepository:
    return ContentRepository(CONTENT_DIR)


def test_there_are_projects_of_both_types() -> None:
    kinds = {path.parent.name for path in PROJECT_FILES}
    assert kinds == set(PROJECT_TYPES)


@pytest.mark.parametrize("path", PROJECT_FILES, ids=lambda p: f"{p.parent.name}/{p.name}")
def test_every_project_file_validates(path: Path) -> None:
    project = load_project(path)
    assert isinstance(project, Project)
    assert project.type == path.parent.name
    assert project.slug == path.stem


def test_repository_loads_every_file(content: ContentRepository) -> None:
    assert len(content.all()) == len(PROJECT_FILES)


def test_skill_aliases_keys_exist_in_projects(content: ContentRepository) -> None:
    used = {skill.lower() for project in content.all() for skill in project.skills}
    unknown = [key for key in content.site["skill_aliases"] if key.lower() not in used]
    assert not unknown, f"skill_aliases keys not used by any project: {unknown}"


def test_chunk_ids_are_unique(content: ContentRepository) -> None:
    ids = [chunk.id for project in content.all() for chunk in project_to_chunks(project)]
    assert len(ids) == len(set(ids))


def make_content_dir(tmp_path: Path, project_text: str, kind: str = "academic") -> Path:
    """A copy of site.yaml plus a single project file."""
    shutil.copy(CONTENT_DIR / "site.yaml", tmp_path / "site.yaml")
    for folder in PROJECT_TYPES:
        (tmp_path / folder).mkdir()
    (tmp_path / kind / "broken-project.md").write_text(project_text, encoding="utf-8")
    return tmp_path


VALID_FRONTMATTER = """\
title: Example
summary: One line.
problem: A problem.
timeline: 2024-01 to 2024-06
skills: [Python]
"""


@pytest.mark.parametrize(
    "frontmatter_text, expected",
    [
        ("title: Missing everything else\n", "summary"),
        (VALID_FRONTMATTER.replace("2024-01 to 2024-06", "Jan 2024"), "YYYY-MM"),
        (VALID_FRONTMATTER.replace("2024-01 to 2024-06", "2024-06 to 2024-01"), "before"),
        (VALID_FRONTMATTER + "unknown_field: 1\n", "unknown_field"),
        (VALID_FRONTMATTER + "slug: custom\n", "set automatically"),
        (VALID_FRONTMATTER + "links: {PDF: paper.pdf}\n", "https://"),
        (
            VALID_FRONTMATTER
            + "decisions:\n  - {id: a, question: Q, options: [X, Y], chose: Z, why: W}\n",
            "must be one of options",
        ),
        (
            VALID_FRONTMATTER
            + "decisions:\n  - {id: problem, question: Q, options: [X, Y], chose: X, why: W}\n",
            "reserved",
        ),
    ],
    ids=["missing-fields", "bad-timeline", "reversed-timeline", "unknown-field", "computed-field",
         "relative-link", "chose-not-an-option", "reserved-decision-id"],
)
def test_malformed_project_fails_loudly(tmp_path: Path, frontmatter_text: str, expected: str) -> None:
    content_dir = make_content_dir(tmp_path, f"---\n{frontmatter_text}---\nBody\n")
    with pytest.raises(ContentError, match=expected):
        ContentRepository(content_dir)


def test_valid_minimal_project_loads(tmp_path: Path) -> None:
    content_dir = make_content_dir(tmp_path, f"---\n{VALID_FRONTMATTER}---\n## Notes\n\nHello.\n", "professional")
    project = ContentRepository(content_dir).get("professional", "broken-project")
    assert project is not None
    assert project.order == 100 and project.featured is False and project.bubble is None
    assert "<h2>Notes</h2>" in project.body_html


def test_missing_site_key_fails(tmp_path: Path) -> None:
    content_dir = make_content_dir(tmp_path, f"---\n{VALID_FRONTMATTER}---\n")
    site = (content_dir / "site.yaml").read_text(encoding="utf-8")
    (content_dir / "site.yaml").write_text(site.replace("tagline:", "tag_line:"), encoding="utf-8")
    with pytest.raises(ContentError, match="tagline"):
        ContentRepository(content_dir)
