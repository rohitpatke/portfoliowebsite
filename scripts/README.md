# scripts/

Run from the repository root.

| Script | Role |
|---|---|
| `freeze.py` | Exports the site to `build/` with Frozen-Flask: one `index.html` per page, static files, `404.html` and `.nojekyll`. Honours `FREEZER_BASE_URL` for sites under a path prefix. |
| `build_index.py` | Stub for the future embedding index. Prints how many chunks would be indexed. |
