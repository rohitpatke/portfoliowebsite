"""FUTURE STUBS: both endpoints return 501 until implemented."""

from __future__ import annotations

from flask import Response, abort, current_app, jsonify

from . import bp


def _not_implemented(feature: str, flag: str) -> tuple[Response, int]:
    if not current_app.config[flag]:
        abort(404)
    return jsonify(error="not_implemented", feature=feature), 501


@bp.post("/chat")
def chat() -> tuple[Response, int]:
    return _not_implemented("chat", "ENABLE_CHAT")


@bp.post("/jd-match")
def jd_match() -> tuple[Response, int]:
    return _not_implemented("jd_match", "ENABLE_JD_MATCH")
