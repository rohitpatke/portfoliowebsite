"""Development server. Use gunicorn in production."""

from __future__ import annotations

import os
from pathlib import Path

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Content is loaded once, so restart when a content file changes.
    content_files = [str(path) for path in Path(app.config["CONTENT_DIR"]).rglob("*") if path.is_file()]
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=app.debug,
        extra_files=content_files,
    )
