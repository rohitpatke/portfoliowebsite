"""FUTURE STUBS: JSON endpoints for the AI features. Both return 501 until implemented.

See README.md, "Roadmap: AI features", for the implementation steps and guardrails.
"""

from __future__ import annotations

from flask import Response, abort, current_app, jsonify

from . import bp


def _not_implemented(feature: str, flag: str) -> tuple[Response, int]:
    if not current_app.config[flag]:
        abort(404)
    return jsonify(error="not_implemented", feature=feature), 501


@bp.post("/chat")
def chat() -> tuple[Response, int]:
    """Answer a question about the projects, citing chunk anchors. Not implemented yet."""
    return _not_implemented("chat", "ENABLE_CHAT")


@bp.post("/jd-match")
def jd_match() -> tuple[Response, int]:
    """Rank projects against a pasted job description. Not implemented yet."""
    return _not_implemented("jd_match", "ENABLE_JD_MATCH")
