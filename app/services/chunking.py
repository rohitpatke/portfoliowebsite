"""Split projects into citable chunks for the future chatbot and JD matcher.

Every chunk's ``anchor`` is an element id on the project's detail page, so an answer can
link straight to its source, for example ``/professional/realtime-fraud-scoring/#feature-store``.
tests/test_routes.py checks that every anchor really exists on the rendered page.
"""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser

from ..models import Project


@dataclass(frozen=True)
class Chunk:
    """One retrievable piece of a project."""

    id: str  # "<type>/<slug>#<anchor>", unique across the site
    project_type: str
    project_slug: str
    project_title: str
    section: str  # summary | problem | decision | outcomes | details
    anchor: str  # element id on the detail page
    text: str


class _TextExtractor(HTMLParser):
    """Collects the text content of an HTML fragment."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def html_to_text(html: str) -> str:
    """Strip tags from rendered Markdown, keeping readable spacing."""
    parser = _TextExtractor()
    parser.feed(html)
    return " ".join(" ".join(parser.parts).split())


def chunk_id(project: Project, anchor: str) -> str:
    """Stable id for a chunk; mirrors the detail-page URL fragment."""
    return f"{project.type}/{project.slug}#{anchor}"


def project_to_chunks(project: Project) -> list[Chunk]:
    """Turn one project into chunks: summary, problem, each decision, outcomes, body."""

    def make(section: str, anchor: str, text: str) -> Chunk:
        return Chunk(
            id=chunk_id(project, anchor),
            project_type=project.type,
            project_slug=project.slug,
            project_title=project.title,
            section=section,
            anchor=anchor,
            text=text,
        )

    meta = ", ".join(
        f"{label}: {value}"
        for label, value in (
            ("Role", project.role), ("Team", project.team), ("Organization", project.org),
            ("Venue", project.venue), ("Timeline", project.timeline),
            ("Skills", ", ".join(project.skills)),
        )
        if value
    )
    chunks = [
        make("summary", "summary", f"{project.title}. {project.summary} ({meta})"),
        make("problem", "problem", project.problem),
    ]
    chunks += [
        make(
            "decision",
            decision.id,
            f"Question: {decision.question} Options: {'; '.join(decision.options)}. "
            f"Chose: {decision.chose}. Why: {decision.why}",
        )
        for decision in project.decisions
    ]
    if project.outcomes:
        outcomes = "; ".join(f"{o.metric}: {o.value}" for o in project.outcomes)
        chunks.append(make("outcomes", "outcomes", outcomes))
    if body := html_to_text(project.body_html):
        chunks.append(make("details", "details", body))
    return chunks
