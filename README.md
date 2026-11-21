# Portfolio

A personal portfolio that separates **academic / research** work from **professional** work
and shows, for every project, the problem, the decisions made along the way and the
outcomes. It is a small Flask + Jinja app that runs live under gunicorn or exports to
static HTML for free hosting. It is structured so that animations and two AI features (a
project chatbot and a job-description matcher) can be added without restructuring.

> **Placeholder content.** Everything under `content/` ("Your Name", Example Payments,
> Placeholder University, example.com links) is sample data. See
> [What to replace](#what-to-replace).

## Contents

1. [Design concept](#1-design-concept)
2. [Quick start](#2-quick-start)
3. [Folder structure](#3-folder-structure)
4. [Adding a project](#4-adding-a-project)
5. [Editing the homepage (`site.yaml`)](#5-editing-the-homepage-siteyaml)
6. [Customizing the design](#6-customizing-the-design)
7. [Adding animation](#7-adding-animation)
8. [Deployment](#8-deployment)
9. [Roadmap: AI features](#9-roadmap-ai-features)
10. [Running tests](#10-running-tests)

---

## 1. Design concept

**Workspace collage.** Like studio sites that show their process instead of describing
it, the page stays minimal (lots of white space, large serif headlines) with a few dense
moments built from work artifacts:

- **Floating cards** around the hero headline: a code snippet, a paper figure with a bar
  chart and a phone mockup.
- **Multiplayer cursors** with role labels ("Researcher", "Engineer"), as in Figma.
- **Comment bubbles** (avatar, "You · 2025", one line) that surface real decisions from the
  projects.
- **Colour encodes track:** violet = academic, teal = professional, gray = neutral.
- **Flat:** 1px hairline borders, 8px / 14px radii, no shadows or gradients.
- **Light and dark** themes follow `prefers-color-scheme`. Every colour is a CSS custom
  property in `tokens.css`, and all text meets WCAG AA contrast in both themes.

Homepage sections, in order: nav · hero collage · what I do · selected work (with filter
pills) · research band (inverse colours) · experience (as notifications) · contact +
recruiter mode.

Detail pages: academic projects use a **research-paper layout** (title, authors, venue,
teaser figure, abstract, decisions, body). Professional projects use a **case-study
layout** (facts, problem, decision cards, outcome tiles, body).

## 2. Quick start

Requires Python 3.11 or newer. No Node.js and no build step.

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

On Windows, activate with `.venv\Scripts\activate` instead.

```bash
pip install -r requirements.txt
```

```bash
cp .env.example .env
```

```bash
python run.py
```

Open <http://127.0.0.1:5000>. Content is loaded once at startup. The dev server restarts
automatically when you edit a file under `content/`, but not when you add a new one, so
restart it yourself after adding a file.

## 3. Folder structure

```
app/                      Flask application package
├── __init__.py           create_app(env): loads content, registers blueprints
├── config.py             Dev/Prod/Test settings and feature flags from env vars
├── models.py             Pydantic models: Project, Decision, Outcome
├── services/             Logic with no HTTP: content loading, chunking, retrieval
├── blueprints/           Page routes: "/" (main.py), "/<kind>/" and "/<kind>/<slug>/" (projects.py)
├── ai/                   FUTURE: /api/chat and /api/jd-match (registered only when flagged on)
├── templates/
│   ├── main/             Homepage and 404 page
│   ├── partials/         Nav, footer, chat widget placeholder
│   ├── components/       Macros: workspace primitives (avatar, cursor, comment), cards
│   ├── sections/         One template per homepage section
│   └── projects/         List page, academic (paper) and professional (case study) layouts
└── static/
    ├── css/              tokens, base, components, sections, motion
    ├── js/               motion.js, filters.js, recruiter.js; effects/ for lazy-loaded animations
    ├── lottie/           Lottie JSON files for effects (empty)
    └── img/              Favicon and images
content/                  All site content: site.yaml plus one Markdown file per project
├── academic/             Research projects (folder name = project type)
└── professional/         Professional projects
scripts/                  freeze.py (static export) and build_index.py (FUTURE stub)
tests/                    pytest suite: content validation and routes
```

Architecture rules:

- Only `ContentRepository` (`app/services/content.py`) reads files. Templates get validated
  objects, and routes stay a few lines long.
- The repository is created once in `create_app` and stored in `app.extensions["content"]`.
  A context processor gives every template `site` (from `site.yaml`) and `features` (the
  AI flags).
- The project type comes from the folder name, and the same two words, `academic` and
  `professional`, are used in models, CSS classes (`track--academic`), data attributes
  (`data-type="academic"`) and filters.
- A malformed project file stops the app at startup with the file path and the Pydantic
  error.

## 4. Adding a project

Create a Markdown file in `content/academic/` or `content/professional/`. The file name
becomes the URL slug, so it must be lowercase words joined by hyphens:
`content/professional/search-ranking.md` → `/professional/search-ranking/`.

The file has YAML frontmatter between `---` lines, then an optional Markdown body (rendered
under the decisions on the detail page).

### Academic example

```markdown
---
title: Few-shot entity recognition for clinical notes
summary: One or two sentences. Used on cards, as the abstract, and as recruiter-mode evidence.
problem: The problem in plain language: who had it and why it mattered.
timeline: 2023-09 to 2024-06            # "YYYY-MM to YYYY-MM"; the card shows the start year
venue: Workshop on Clinical NLP 2024    # shown under the title
authors: [A. Coauthor, Your Name, B. Advisor]   # your name (site.yaml `name`) is underlined
role: Shared first author               # optional
skills: [Python, PyTorch, NLP]          # required; drives recruiter-mode matching
links:                                  # label → URL (https://, http:// or mailto:)
  PDF: https://arxiv.org/abs/0000.00000
  Code: https://github.com/you/repo
  Slides: https://example.com/slides
decisions:
  - id: error-analysis-first            # becomes the anchor #error-analysis-first
    question: Where should the first month go?
    options: [Tune the architecture, Error analysis on the baseline]
    chose: Error analysis on the baseline   # must match one of `options` exactly
    why: Two thirds of errors came from abbreviations; no architecture change would fix that.
    bubble: Spent a month on error analysis before touching the model.   # optional
outcomes:
  - metric: F1 with 10% of labels
    value: 87.1
featured: true      # show on the homepage
order: 10           # lower comes first (default 100)
hero_effect: lottie # optional: lottie | gsap | three (see section 7)
---

## Approach

Free-form Markdown: headings, lists, tables, code blocks.
```

### Professional example

```markdown
---
title: Real-time fraud scoring service
summary: Replaced a nightly batch model with a streaming service that decides at checkout.
problem: Fraud was detected after goods had shipped; decisions had to fit a 100 ms budget.
timeline: 2025-01 to 2025-09
role: ML Engineer                     # card shows "role · team"
team: Risk Platform, 5 engineers
org: Example Payments                 # shown in the case-study header
skills: [Python, Machine Learning, Kafka, Kubernetes, SQL]
links:
  Write-up: https://example.com/blog/realtime-fraud
decisions:
  - id: streaming-features
    question: Where should real-time features be computed?
    options: [In the request path, In a streaming feature store]
    chose: In a streaming feature store
    why: Request-path aggregation blew the p95 budget; precomputing kept scoring under 40 ms.
    bubble: Moved feature computation out of the request path to keep p95 under 40 ms.
outcomes:                             # the first two appear as metric tiles on the card
  - metric: p95 scoring latency
    value: 38 ms
  - metric: Fraud losses
    value: −18%
featured: true
order: 10
---
```

### How the special fields work

| Field | Effect |
|---|---|
| `featured` | `true` puts the project in the homepage "Selected work" grid. All projects always appear on their list page (`/academic/`, `/professional/`), and academic projects also appear in the research band. |
| `order` | Sort key everywhere, ascending (default 100). Projects with the same `order` are sorted newest first, by the end of `timeline`. |
| `bubble` | One-line version of a decision. The **first** decision with a `bubble` is shown as a comment bubble on the project's card. |
| `decisions[].id` | Lowercase slug, unique within the project. It is the element id on the detail page (`/professional/slug/#streaming-features`) **and** the chunk anchor used by the future chatbot. It cannot be `summary`, `problem`, `decisions`, `outcomes`, `details` or `main`, which are page sections. |
| `skill_aliases` | In `site.yaml`, not in the project file: alternate terms recruiters use for a skill, e.g. `Kubernetes: [k8s]`. Recruiter mode matches the skill name or any alias as a whole word, case-insensitively. Every key must be a skill used by at least one project; a test enforces this. |

Validation (startup fails with a clear message if any rule is broken): unknown keys are
rejected, `title`, `summary`, `problem`, `timeline` and at least one skill are required,
the timeline must be `YYYY-MM to YYYY-MM` with the end not before the start, links must be
absolute URLs, each decision needs at least two options, and `chose` must be one of them.
`slug`, `type` and `body_html` are computed and must not appear in frontmatter.

## 5. Editing the homepage (`site.yaml`)

All homepage text that is not a section heading lives in `content/site.yaml`:

| Key | Used for |
|---|---|
| `name`, `initials` | Nav, footer, avatars; `name` is underlined in author lists |
| `tagline` | Pill above the hero headline |
| `headline` | Hero `<h1>` |
| `status` | Comment bubble in the contact section ("You · now") |
| `email`, `linkedin` | Contact buttons and footer |
| `hero.code_file`, `hero.code_lines` | File name and lines in the floating code card |
| `hero.figure_caption`, `hero.figure_bars` | Caption and bar heights (percent) of the figure card; the bars are reused on academic teasers |
| `hero.comment` | `{year, text, track}` for the hero comment bubble |
| `hero.cursors` | `[{label, track}]`; the first sits on the figure card, the second on the code card |
| `hero.tools` | Tabler icon names (without `ti-`), e.g. `brand-python`; browse at <https://tabler.io/icons> |
| `services` | "What I do" cards: `{icon, title, text, track}` |
| `experience` | Timeline entries `{year, text}`, newest first |
| `organizations` | Muted row of names under the timeline |
| `skill_aliases` | See section 4 |

`track` is always `academic`, `professional` or `neutral`. The phone mockup shows the first
featured professional project (title and first two outcomes), so it needs no settings.

## 6. Customizing the design

**Tokens.** Every colour, font, size, radius and duration is a custom property in
`app/static/css/tokens.css`. The light theme is in `:root`; the dark theme overrides the
same names inside `@media (prefers-color-scheme: dark)`. Change a value once and it
applies everywhere. Keep text colours at 4.5:1 contrast or better against `--color-bg`,
`--color-surface` and `--color-surface-2`.

**Track colours.** `.track--academic`, `.track--professional` and `.track--neutral` set
three variables, `--track`, `--track-soft` and `--track-line`, and components only ever read
those. To recolour a track, change `--color-academic*` / `--color-professional*` (and their
dark-theme and `--inverse-*` versions). To make any element track-coloured, add the class:
`<div class="metric track--academic">`.

**Inverse areas.** `.inverse` re-points the base tokens to the `--inverse-*` palette, so
everything inside renders inverted (dark on the light theme, light on the dark theme).
The research band uses it, and you can reuse it for any callout.

**Stylesheets.** `base.css` holds reset, typography and prose; `components.css` holds
reusable pieces (buttons, cards, comment, cursor, metric, decision, forms); `sections.css`
holds page regions and layouts; `motion.css` holds everything that moves.

**Adding a homepage section:**

1. Create `app/templates/sections/home_<name>.html`. Start it with
   `<section class="section" id="<name>" aria-labelledby="<name>-title">`, a `.container`
   and a `<header class="section__header">` with an `<h2 id="<name>-title" class="section__title">`.
   Use `h2` for the section and `h3` inside it; each page has exactly one `h1`.
2. If it needs card macros, start with `{% import "components/cards.html" as cards with context %}`.
3. Put its data in `site.yaml` (and in `SITE_REQUIRED_KEYS` in `app/services/content.py` if
   it is required), or pass it from `blueprints/main.py`. Templates never read files.
4. Add `{% include "sections/home_<name>.html" %}` to `app/templates/main/index.html`.
5. Put its styles in `sections.css` under a `/* ---------- Name ---------- */` heading.
6. Add `data-animate` (and `style="--delay: N"` for staggered siblings) to anything that
   should reveal on scroll.

## 7. Adding animation

Motion comes in three layers. All of them respect `prefers-reduced-motion`: with reduced
motion, nothing moves, nothing is hidden and no effect modules load.

| Level | Where | What it does |
|---|---|---|
| 1. CSS | `motion.css` | Hover lift on `.card--interactive`; hero pieces fade in and gently `drift`; cursors wander; `@view-transition { navigation: auto; }` cross-fades between pages. |
| 2. Scroll reveal | `motion.js` | `IntersectionObserver` adds `.is-visible` to `[data-animate]` elements as they enter the viewport. Set `style="--delay: 2"` to stagger (each step is `--stagger`, 90ms). |
| 3. Effect loader | `motion.js` + `static/js/effects/` | `[data-effect="lottie\|gsap\|three"]` lazily `import()`s `effects/<name>.js` when the element nears the viewport and calls its default export with the element. |

**Content never stays hidden.** An inline script in `base.html` adds a `js` class to
`<html>`, and the hiding rules only apply under `.js`. If `motion.js` has not started
within 3 seconds (blocked, offline, old browser), the class is removed again. Printing
always shows everything.

**Where effects mount.** A project with `hero_effect` in its frontmatter gets
`data-effect` and `data-project="<slug>"` on its teaser figure (academic pages) or its
case-study header (professional pages). Without an effect module the static fallback
stays, and the console shows a warning.

### Worked example: a Lottie teaser for an academic project

1. Export your animation from After Effects (Bodymovin) or download one from LottieFiles,
   and save it as `app/static/lottie/<project-slug>.json`, for example
   `app/static/lottie/clinical-entity-recognition.json`.

2. Create `app/static/js/effects/lottie.js`:

   ```js
   // Plays static/lottie/<data-project>.json inside the teaser, replacing the static bars.
   export default async function mount(element) {
     const { default: lottie } = await import("https://cdn.jsdelivr.net/npm/lottie-web@5.12.2/+esm");
     const canvas = element.querySelector(".teaser__canvas") ?? element;

     const holder = document.createElement("div");
     holder.className = "teaser__lottie";
     holder.hidden = true;
     canvas.append(holder);

     const animation = lottie.loadAnimation({
       container: holder,
       renderer: "svg",
       loop: true,
       autoplay: true,
       // Relative to this module, so it also works under a URL prefix.
       path: new URL(`../../lottie/${element.dataset.project}.json`, import.meta.url).href,
     });

     await new Promise((resolve, reject) => {
       animation.addEventListener("DOMLoaded", resolve);
       animation.addEventListener("data_failed", () => reject(new Error("Lottie JSON failed to load")));
     });

     // Swap the fallback for the animation only once it is ready.
     canvas.querySelectorAll(".teaser__bar").forEach((bar) => bar.remove());
     holder.hidden = false;
   }
   ```

3. Give it room in `app/static/css/components.css`:

   ```css
   .teaser__lottie {
     flex: 1;
     align-self: stretch;
     min-height: 12rem;
   }
   ```

4. Turn it on in the project's frontmatter:

   ```yaml
   hero_effect: lottie
   ```

5. Reload the project page. The element's `data-effect-state` attribute goes from
   `loading` to `ready`; if it ends as `failed`, the console says why and the bars stay.

GSAP and Three.js work the same way: `effects/gsap.js` or `effects/three.js`, each with a
default export that receives the element. `static/js/effects/README.md` has a GSAP
example. Load libraries inside the function, pinned to an exact version, so pages that
don't use them never download them.

## 8. Deployment

### Static (free): freeze, then upload `build/`

```bash
python scripts/freeze.py
```

This writes `build/` with one `index.html` per page, the static files, a `404.html` and a
`.nojekyll` file. If the site will live under a path prefix (a GitHub Pages *project*
site such as `https://you.github.io/portfolio/`), set the prefix when freezing:

```bash
FREEZER_BASE_URL=https://you.github.io/portfolio/ python scripts/freeze.py
```

Recruiter mode works on the static site because matching runs in the browser. The future
AI endpoints need a live server.

**GitHub Pages.** In the repository go to *Settings → Pages → Source: GitHub Actions*,
then add `.github/workflows/pages.yml`:

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python scripts/freeze.py
        env:
          # Remove this line for a user site (you.github.io) or a custom domain.
          FREEZER_BASE_URL: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/
      - uses: actions/upload-pages-artifact@v3
        with:
          path: build
      - id: deployment
        uses: actions/deploy-pages@v4
```

**Netlify.** *Add new site → Import from Git*, then set:
- Build command: `pip install -r requirements.txt && python scripts/freeze.py`
- Publish directory: `build`
- Environment variable: `PYTHON_VERSION` = `3.11`

**Cloudflare Pages.** *Workers & Pages → Create → Pages → Connect to Git*, then set:
- Build command: `pip install -r requirements.txt && python scripts/freeze.py`
- Build output directory: `build`
- Environment variable: `PYTHON_VERSION` = `3.11`

Both hosts serve `build/404.html` for unknown URLs.

### Live (gunicorn)

Use a live deployment when you turn on the AI features. Locally:

```bash
gunicorn "app:create_app('production')" --bind 0.0.0.0:8000 --workers 2
```

Set `SECRET_KEY` (a long random string) and any feature flags as environment variables on
the host. Never commit `.env`.

**Render.** *New → Web Service*, connect the repository, then set:
- Runtime: Python 3, with environment variable `PYTHON_VERSION` = `3.11.9`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn "app:create_app('production')" --bind 0.0.0.0:$PORT --workers 2`

**Railway.** *New Project → Deploy from GitHub repo*. Under *Settings → Deploy*, set the
custom start command to:
```bash
gunicorn "app:create_app('production')" --bind 0.0.0.0:$PORT --workers 2
```
Railway installs `requirements.txt` automatically.

**Fly.io.** Add this `Dockerfile` at the repository root:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
CMD gunicorn "app:create_app('production')" --bind 0.0.0.0:$PORT --workers 2
```

Then run:

```bash
fly launch --internal-port 8080
```

```bash
fly secrets set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

```bash
fly deploy
```

## 9. Roadmap: AI features

### Already scaffolded

| Piece | Where | State |
|---|---|---|
| Feature flags | `.env`: `ENABLE_CHAT`, `ENABLE_JD_MATCH` → `app.config`, and `features` in templates | Working |
| `ai` blueprint | `app/ai/`: `POST /api/chat`, `POST /api/jd-match` | Registered only when a flag is on; each route returns 404 when its own flag is off, otherwise **501** |
| Prompts | `app/ai/prompts.py` | Placeholder system prompts with grounding and citation rules |
| Chunking | `app/services/chunking.py` | `project_to_chunks()` turns each project into summary, problem, per-decision, outcomes and body chunks. The chunk id is `<type>/<slug>#<anchor>`, and every anchor is an element id on the detail page (a test enforces this). |
| Retrieval | `app/services/retrieval.py` | `Retriever` protocol plus `FullContextRetriever`, which returns every chunk (the whole portfolio fits in one prompt) |
| Embedding index | `scripts/build_index.py` | Stub; prints the chunk count and "not implemented" |
| Chat UI | `partials/chat_widget.html` | Disabled placeholder, rendered only when `ENABLE_CHAT=true` |
| JD matcher UI | `static/js/recruiter.js` | Working client-side keyword matcher, with a marked swap point in `findMatches()` for `fetch('/api/jd-match')` |

### Chatbot: steps

1. Add the model SDK to `requirements.txt`, for example `anthropic`, and keep the API key
   in the host's environment (`ANTHROPIC_API_KEY`), never in the repository.
2. At startup, build `FullContextRetriever([c for p in content.all() for c in project_to_chunks(p)])`
   and store it in `app.extensions`.
3. In `chat()`: validate the JSON body (`question`: a string of at most 500 characters),
   retrieve chunks, format them as `<chunk id="...">text</chunk>`, fill `CHAT_SYSTEM_PROMPT`
   and call the model. With the Anthropic SDK:

   ```python
   import anthropic

   client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
   response = client.beta.messages.create(
       model="claude-opus-5-5",
       max_tokens=16000,
       output_config={"effort": "low"},            # short, factual answers
       betas=["server-side-fallback-2026-07-01"],
       fallbacks="default",                        # re-run on a fallback model if declined
       system=CHAT_SYSTEM_PROMPT.format(name=site["name"], email=site["email"], chunks=chunks_xml),
       messages=[{"role": "user", "content": question}],
   )
   if response.stop_reason == "refusal":
       answer = "Sorry, I can't help with that one."
   else:
       answer = "".join(block.text for block in response.content if block.type == "text")
   ```

4. Parse the `[type/slug#anchor]` citations, **drop any id that is not a real chunk**, and
   return `{"answer": ..., "sources": [{"id", "title", "url"}]}`, where each `url` is
   `url_for("projects.detail", ...) + "#" + anchor`.
5. Replace the placeholder form in `chat_widget.html` with a small ES module that posts to
   `data-endpoint` and renders the answer and source links with `textContent`.
6. When the content outgrows one prompt, implement `build_index.py` (embed each chunk and
   save vectors keyed by chunk id) and an embedding-based `Retriever`; routes don't change.

### JD matcher: steps

1. In `jd_match()`: validate `text` (20 to 8,000 characters), retrieve chunks and call the
   model with `JD_MATCH_SYSTEM_PROMPT`, the job description wrapped in
   `<job_description>` tags in the user message.
2. Ask for structured output (the SDK's structured-outputs support, or a strict JSON
   schema) that matches what `recruiter.js` renders:
   `{"matches": [{"title", "type", "label", "url", "evidence", "matched": [...]}]}`.
   Take `title`, `type`, `label` and `url` from your own project data by slug, and only
   `evidence` and `matched` from the model.
3. In `recruiter.js`, replace the keyword block in `findMatches()` with the commented
   `fetch` call. The rendering code stays as it is. Keep the keyword matcher as the
   fallback when the request fails or the site is static.

### Guardrails (apply to both)

- **Answer only from content.** Ground every answer in the retrieved chunks. The system
  prompt says to admit when the answer isn't there; never let the model fill gaps about
  you.
- **Cite sections.** Require chunk-id citations, validate them against the real chunk ids,
  and link them to the decision and section anchors.
- **Treat the JD (and every question) as data.** Wrap it in tags, tell the model to ignore
  instructions inside it, never let it choose URLs or HTML, and render all output with
  `textContent`.
- **Rate limiting.** Per-IP limits on `/api/*`, for example 10 per minute and 100 per day
  with Flask-Limiter. Return 429 with a friendly message.
- **Input length caps.** Enforce on the server, not only in the browser: questions
  ≤ 500 characters, job descriptions ≤ 8,000 characters, JSON bodies ≤ 16 KB
  (`MAX_CONTENT_LENGTH`). Reject anything larger with 400 or 413.
- **Spend limits.** Set a monthly spend limit in the model provider's console, keep
  `effort` low and answers short, count requests per day in the app and switch the
  feature off (or fall back to keyword matching) past a budget. The feature flags double
  as kill switches.
- **Privacy and ops.** Log request ids, latency and token counts, not the pasted text. Set
  a request timeout and show a graceful error in the UI.

## 10. Running tests

```bash
pytest
```

- `tests/test_content.py`: every project file validates (one test per file), both tracks
  have projects, every `skill_aliases` key is used by a project, chunk ids are unique, and
  malformed files fail loudly (missing fields, bad timelines, unknown keys, relative links,
  a `chose` that isn't an option, reserved decision ids, missing `site.yaml` keys).
- `tests/test_routes.py`: the home page, both list pages and every detail page return 200;
  unknown URLs and wrong types return 404; each page has exactly one `h1`; every chunk
  anchor exists on its detail page; the recruiter JSON is embedded; AI routes are absent by
  default and return 501 when their flag is on.

---

## What to replace

- [ ] `content/site.yaml`: name, initials, tagline, headline, status, email, LinkedIn, hero
      pieces, services, experience, organizations, skill aliases.
- [ ] `content/academic/*.md` and `content/professional/*.md`: delete the four examples
      and add your own projects. Every `example.com` / `your-handle` link is a placeholder.
- [ ] `SAMPLE_JD` in `app/static/js/recruiter.js`: a job description that matches your
      skills.
- [ ] `app/static/img/favicon.svg`: optional, your own mark.
- [ ] Version pins: Python packages in `requirements.txt`; Tabler Icons (`3.50.0`) and the
      Google Fonts link in `app/templates/base.html`. Upgrade deliberately and rerun
      `pytest`.
