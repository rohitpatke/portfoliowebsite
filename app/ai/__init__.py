"""FUTURE: AI features (project chatbot, job-description matcher).

Registered by ``create_app`` only when ENABLE_CHAT or ENABLE_JD_MATCH is true.
Each route also checks its own flag, so enabling one feature does not expose the other.
"""

from flask import Blueprint

bp = Blueprint("ai", __name__, url_prefix="/api")

from . import routes  # noqa: E402,F401  (registers the routes on bp)
