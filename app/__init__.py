"""Application factory."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from flask import Flask, render_template

from .config import get_config
from .services.content import ContentRepository


def create_app(env: str | None = None) -> Flask:
    """Build the app for ``env`` (development, production or testing; default: $APP_ENV).

    Content is loaded and validated here, so a malformed project file stops startup.
    """
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(get_config(env or os.getenv("APP_ENV", "development")))

    content = ContentRepository(Path(app.config["CONTENT_DIR"]))
    app.extensions["content"] = content

    features = {"chat": app.config["ENABLE_CHAT"], "jd_match": app.config["ENABLE_JD_MATCH"]}

    @app.context_processor
    def inject_globals() -> dict[str, Any]:
        return {"site": content.site, "features": features}

    from .blueprints.main import bp as main_bp
    from .blueprints.projects import bp as projects_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(projects_bp)

    if features["chat"] or features["jd_match"]:
        from .ai import bp as ai_bp

        app.register_blueprint(ai_bp)

    @app.errorhandler(404)
    def not_found(_error: Exception) -> tuple[str, int]:
        return render_template("main/404.html"), 404

    return app
