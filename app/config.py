"""Environment-specific settings and feature flags.

Values that come from environment variables are read when ``create_app`` runs
(not at import time), so tests and scripts can set them just before building an app.
"""

from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent

TRUTHY = {"1", "true", "yes", "on"}


def env_flag(name: str, default: bool = False) -> bool:
    """Read a boolean feature flag such as ``ENABLE_CHAT=true`` from the environment."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in TRUTHY


class Config:
    """Settings shared by every environment."""

    DEBUG = False
    TESTING = False
    CONTENT_DIR = BASE_DIR / "content"

    # Frozen-Flask (static export, see scripts/freeze.py)
    FREEZER_DESTINATION = str(BASE_DIR / "build")
    FREEZER_STATIC_IGNORE = ["README.md", ".gitkeep"]

    @classmethod
    def as_dict(cls) -> dict[str, Any]:
        """Return class defaults merged with values read from the environment right now."""
        settings: dict[str, Any] = {key: getattr(cls, key) for key in dir(cls) if key.isupper()}
        settings.update(
            # No sessions or forms use this today; a random fallback keeps prod safe by default.
            SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
            ENABLE_CHAT=env_flag("ENABLE_CHAT"),
            ENABLE_JD_MATCH=env_flag("ENABLE_JD_MATCH"),
        )
        if base_url := os.getenv("FREEZER_BASE_URL"):
            settings["FREEZER_BASE_URL"] = base_url
        return settings


class DevConfig(Config):
    """Local development: debug pages and template auto-reload."""

    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class ProdConfig(Config):
    """Production (gunicorn) and static export."""


class TestConfig(Config):
    """pytest."""

    TESTING = True


CONFIGS: dict[str, type[Config]] = {
    "development": DevConfig,
    "production": ProdConfig,
    "testing": TestConfig,
}


def get_config(env: str) -> dict[str, Any]:
    """Return the settings dict for ``env`` (development, production or testing)."""
    try:
        config_class = CONFIGS[env]
    except KeyError:
        valid = ", ".join(sorted(CONFIGS))
        raise ValueError(f"Unknown APP_ENV {env!r}; expected one of: {valid}") from None
    return config_class.as_dict()
