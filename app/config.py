"""Settings per environment. Env vars are read in ``get_config``, not at import time."""

from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"

ENVIRONMENTS: dict[str, dict[str, Any]] = {
    "development": {"DEBUG": True},
    "production": {},
    "testing": {"TESTING": True},
}


def env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def get_config(env: str) -> dict[str, Any]:
    if env not in ENVIRONMENTS:
        raise ValueError(f"Unknown APP_ENV {env!r}; expected one of: {', '.join(ENVIRONMENTS)}")
    settings: dict[str, Any] = {
        "CONTENT_DIR": CONTENT_DIR,
        "SECRET_KEY": os.getenv("SECRET_KEY") or secrets.token_hex(32),
        "ENABLE_CHAT": env_flag("ENABLE_CHAT"),
        "ENABLE_JD_MATCH": env_flag("ENABLE_JD_MATCH"),
        "FREEZER_DESTINATION": str(BASE_DIR / "build"),
        "FREEZER_STATIC_IGNORE": ["README.md", ".gitkeep"],
        **ENVIRONMENTS[env],
    }
    if base_url := os.getenv("FREEZER_BASE_URL"):
        settings["FREEZER_BASE_URL"] = base_url
    return settings
