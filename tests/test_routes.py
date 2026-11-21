"""Every page renders, unknown URLs are 404s, and AI routes follow their feature flags."""

from __future__ import annotations

import json
import re
from collections.abc import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import Config
from app.services.chunking import project_to_chunks
from app.services.content import ContentRepository

PROJECTS = ContentRepository(Config.CONTENT_DIR).all()


@pytest.fixture()
def app(monkeypatch: pytest.MonkeyPatch) -> Iterator[Flask]:
    monkeypatch.setenv("ENABLE_CHAT", "false")
    monkeypatch.setenv("ENABLE_JD_MATCH", "false")
    yield create_app("testing")


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def detail_url(project) -> str:
    return f"/{project.type}/{project.slug}/"


def test_home(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    for anchor in ('id="work"', 'id="research"', 'id="experience"', 'id="contact"'):
        assert anchor in html


@pytest.mark.parametrize("path", ["/academic/", "/professional/"])
def test_list_pages(client: FlaskClient, path: str) -> None:
    assert client.get(path).status_code == 200


@pytest.mark.parametrize("project", PROJECTS, ids=detail_url)
def test_every_detail_page(client: FlaskClient, project) -> None:
    response = client.get(detail_url(project))
    assert response.status_code == 200
    assert project.title in response.get_data(as_text=True)


@pytest.mark.parametrize(
    "path",
    ["/does-not-exist/", "/research/", "/academic/no-such-project/", "/professional/no-such-project/"],
)
def test_unknown_urls_are_404(client: FlaskClient, path: str) -> None:
    response = client.get(path)
    assert response.status_code == 404
    assert "This page isn" in response.get_data(as_text=True)


def test_project_under_the_wrong_type_is_404(client: FlaskClient) -> None:
    project = PROJECTS[0]
    other = "academic" if project.type == "professional" else "professional"
    assert client.get(f"/{other}/{project.slug}/").status_code == 404


@pytest.mark.parametrize(
    "path", ["/", "/academic/", "/professional/", "/missing/", *map(detail_url, PROJECTS)]
)
def test_exactly_one_h1(client: FlaskClient, path: str) -> None:
    html = client.get(path).get_data(as_text=True)
    assert len(re.findall(r"<h1[\s>]", html)) == 1


@pytest.mark.parametrize("project", PROJECTS, ids=detail_url)
def test_chunk_anchors_exist_on_detail_page(client: FlaskClient, project) -> None:
    """The chatbot will cite chunk anchors; each must be an element id on the page."""
    html = client.get(detail_url(project)).get_data(as_text=True)
    for chunk in project_to_chunks(project):
        assert f'id="{chunk.anchor}"' in html, f"missing #{chunk.anchor} for {chunk.id}"


def test_recruiter_data_is_embedded(client: FlaskClient) -> None:
    html = client.get("/").get_data(as_text=True)
    match = re.search(r'<script type="application/json" id="recruiter-data">(.*?)</script>', html, re.S)
    assert match, "recruiter-data script tag missing"
    records = json.loads(match.group(1))
    assert {record["url"] for record in records} == {detail_url(p) for p in PROJECTS}
    for record in records:
        assert record["type"] in ("academic", "professional")
        for skill in record["skills"]:
            assert skill["terms"] and all(term == term.lower() for term in skill["terms"])


def test_ai_routes_absent_by_default(client: FlaskClient) -> None:
    assert client.post("/api/chat").status_code == 404
    assert client.post("/api/jd-match").status_code == 404
    assert "chat-widget" not in client.get("/").get_data(as_text=True)


def test_ai_routes_follow_their_own_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENABLE_CHAT", "true")
    monkeypatch.setenv("ENABLE_JD_MATCH", "false")
    client = create_app("testing").test_client()

    response = client.post("/api/chat", json={"question": "hi"})
    assert response.status_code == 501
    assert response.get_json() == {"error": "not_implemented", "feature": "chat"}
    assert client.post("/api/jd-match").status_code == 404
    assert "chat-widget" in client.get("/").get_data(as_text=True)
