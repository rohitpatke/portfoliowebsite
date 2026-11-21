"""Pydantic models for project content, validated at startup."""

from __future__ import annotations

import re
from typing import Annotated, Literal, get_args

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ProjectType = Literal["academic", "professional"]
PROJECT_TYPES: tuple[ProjectType, ...] = get_args(ProjectType)
TYPE_LABELS: dict[str, str] = {"academic": "Research", "professional": "Professional"}

EffectName = Literal["lottie", "gsap", "three"]

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TIMELINE_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2]) to \d{4}-(0[1-9]|1[0-2])$")
LINK_PREFIXES = ("https://", "http://", "mailto:")

# Detail-page section ids, also used as chunk anchors; decision ids may not reuse them.
SECTION_ANCHORS = frozenset({"main", "summary", "problem", "decisions", "outcomes", "details"})

# Set by ContentRepository, never in frontmatter.
COMPUTED_FIELDS = frozenset({"slug", "type", "body_html"})

Text = Annotated[str, Field(min_length=1)]


class ContentModel(BaseModel):
    # coerce_numbers_to_str lets YAML like `value: 87.1` fill a text field.
    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True, frozen=True, coerce_numbers_to_str=True
    )


class Decision(ContentModel):
    id: str
    question: Text
    options: list[Text] = Field(min_length=2)
    chose: Text
    why: Text
    bubble: Text | None = None

    @field_validator("id")
    @classmethod
    def _id_is_anchor_safe(cls, value: str) -> str:
        if not SLUG_RE.match(value):
            raise ValueError("must be a lowercase slug such as 'pick-a-database'")
        if value in SECTION_ANCHORS:
            raise ValueError(f"'{value}' is reserved for a page section; choose another id")
        return value

    @model_validator(mode="after")
    def _chose_is_an_option(self) -> Decision:
        if self.chose not in self.options:
            raise ValueError(f"chose {self.chose!r} must be one of options {self.options}")
        return self


class Outcome(ContentModel):
    metric: Text
    value: Text


class Project(ContentModel):
    title: Text
    summary: Text
    problem: Text
    timeline: str
    skills: list[Text] = Field(min_length=1)
    role: Text | None = None
    team: Text | None = None
    org: Text | None = None
    venue: Text | None = None
    authors: list[Text] = Field(default_factory=list)
    links: dict[Text, str] = Field(default_factory=dict)
    decisions: list[Decision] = Field(default_factory=list)
    outcomes: list[Outcome] = Field(default_factory=list)
    featured: bool = False
    order: int = 100
    hero_effect: EffectName | None = None

    slug: str
    type: ProjectType
    body_html: str = ""

    @field_validator("slug")
    @classmethod
    def _slug_format(cls, value: str) -> str:
        if not SLUG_RE.match(value):
            raise ValueError("file name must be a lowercase slug such as 'my-project.md'")
        return value

    @field_validator("timeline")
    @classmethod
    def _timeline_format(cls, value: str) -> str:
        if not TIMELINE_RE.match(value):
            raise ValueError("must look like 'YYYY-MM to YYYY-MM'")
        start, end = value.split(" to ")
        if end < start:
            raise ValueError("end month is before start month")
        return value

    @field_validator("skills")
    @classmethod
    def _skills_unique(cls, value: list[str]) -> list[str]:
        lowered = [skill.lower() for skill in value]
        if len(set(lowered)) != len(lowered):
            raise ValueError("skills contain duplicates")
        return value

    @field_validator("links")
    @classmethod
    def _links_absolute(cls, value: dict[str, str]) -> dict[str, str]:
        for label, url in value.items():
            if not url.startswith(LINK_PREFIXES):
                raise ValueError(f"link {label!r} must start with https://, http:// or mailto:")
        return value

    @field_validator("decisions")
    @classmethod
    def _decision_ids_unique(cls, value: list[Decision]) -> list[Decision]:
        ids = [decision.id for decision in value]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        if duplicates:
            raise ValueError(f"duplicate decision ids: {', '.join(duplicates)}")
        return value

    @property
    def year(self) -> str:
        return self.timeline[:4]

    @property
    def ends(self) -> str:
        return self.timeline.split(" to ")[1]

    @property
    def bubble(self) -> Decision | None:
        return next((decision for decision in self.decisions if decision.bubble), None)

    @property
    def type_label(self) -> str:
        return TYPE_LABELS[self.type]
