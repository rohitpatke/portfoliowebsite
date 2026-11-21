# Portfolio

A Flask + Jinja portfolio that separates **research** from **professional** work and shows,
for every project, the problem, the decisions and the outcomes. It runs live under gunicorn
or exports to static HTML for free hosting.

> Everything under `content/` is placeholder data. See [What to replace](#what-to-replace).

## Quick start

Requires Python 3.11+. No Node.js, no build step.

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
cp .env.example .env
```

```bash
python run.py
```

Open <http://127.0.0.1:5000>. Content is loaded once at startup: the dev server restarts when
you edit a file under `content/`, but restart it yourself after adding a new one.

## Where things are

Each folder has its own `README.md` with the details.

| Folder | What it holds |
|---|---|
| [`content/`](content/README.md) | All site text: `site.yaml` and one Markdown file per project |
| [`app/`](app/README.md) | The Flask app: factory, config, models |
| [`app/services/`](app/services/README.md) | Content loading, chunking, retrieval (no HTTP) |
| [`app/blueprints/`](app/blueprints/README.md) | Page routes |
| [`app/ai/`](app/ai/README.md) | Future AI endpoints and the plan for building them |
| [`app/templates/`](app/templates/README.md) | Jinja pages, sections and macros |
| [`app/static/`](app/static/README.md) | CSS, JS, images; design tokens and motion |
| [`scripts/`](scripts/README.md) | Static export and the embedding-index stub |
| [`tests/`](tests/README.md) | pytest suite |

## Adding a project

Add `content/academic/<slug>.md` or `content/professional/<slug>.md`. The folder sets the
type and the file name becomes the URL (`/professional/<slug>/`). The full field reference
is in [`content/README.md`](content/README.md); a malformed file stops startup with a clear
error.

## Deployment

**Static (free).** Recruiter mode works here because matching runs in the browser.

```bash
python scripts/freeze.py
```

Upload `build/` to GitHub Pages, Netlify or Cloudflare Pages (build command
`pip install -r requirements.txt && python scripts/freeze.py`, output `build`). For a site
under a path prefix, such as a GitHub Pages project site, set the prefix when freezing:

```bash
FREEZER_BASE_URL=https://you.github.io/portfolio/ python scripts/freeze.py
```

**Live (needed for the AI features).** Set `SECRET_KEY` and any feature flags as environment
variables on the host (Render, Railway, Fly.io, ...) and start with:

```bash
gunicorn "app:create_app('production')" --bind 0.0.0.0:$PORT --workers 2
```

## Tests

```bash
pytest
```

## What to replace

- [ ] `content/site.yaml`: name, contact details, hero pieces, services, experience, skill aliases.
- [ ] `content/academic/*.md`, `content/professional/*.md`: replace the four examples.
- [ ] `SAMPLE_JD` in `app/static/js/recruiter.js`: a job description that fits your skills.
- [ ] `app/static/img/favicon.svg` (optional).
- [ ] Version pins in `requirements.txt` and the Tabler Icons / Google Fonts links in
      `app/templates/base.html`. Upgrade deliberately and rerun `pytest`.
