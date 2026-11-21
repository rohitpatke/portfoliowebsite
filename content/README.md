# content/

All site text. Nothing here is code; `app/services/content.py` loads and validates it once at
startup, so a mistake stops the app with the file path and the reason.

- `site.yaml`: homepage settings.
- `academic/`, `professional/`: one Markdown file per project. Keep only project files in
  these two folders (every `*.md` there is loaded as a project).

## Project files

The file name is the slug (lowercase words joined by hyphens). YAML frontmatter goes between
`---` lines; the optional Markdown body is rendered below the decisions on the detail page.

```markdown
---
title: Real-time fraud scoring service              # required
summary: One or two sentences for cards and recruiter mode.   # required
problem: Who had the problem and why it mattered.   # required
timeline: 2025-01 to 2025-09                        # required, "YYYY-MM to YYYY-MM"
skills: [Python, Kafka, SQL]                        # required, drives recruiter matching
role: ML Engineer
team: Risk Platform, 5 engineers
org: Example Payments                               # professional header
venue: Workshop on Clinical NLP 2024                # academic, under the title
authors: [A. Coauthor, Your Name]                   # site.yaml `name` is underlined
links: {PDF: https://..., Code: https://...}        # https://, http:// or mailto:
decisions:
  - id: streaming-features                          # anchor on the detail page
    question: Where should real-time features be computed?
    options: [In the request path, In a streaming feature store]   # at least two
    chose: In a streaming feature store             # must match an option exactly
    why: Request-path aggregation blew the p95 budget.
    bubble: Moved features out of the request path.  # optional card comment
outcomes:
  - metric: p95 scoring latency
    value: 38 ms
featured: true        # show on the homepage
order: 10             # lower first (default 100); ties sort newest first
hero_effect: lottie   # optional: lottie | gsap | three (see app/static/js/effects/)
---

## Free-form Markdown body
```

Rules: unknown keys are errors; `slug`, `type` and `body_html` are computed and must not be
set; the timeline end can't be before its start; decision ids must be unique slugs and can't
be `main`, `summary`, `problem`, `decisions`, `outcomes` or `details` (page sections). The
first decision with a `bubble` shows as a comment on the card; professional cards show the
first two outcomes.

## site.yaml

| Key | Used for |
|---|---|
| `name`, `initials` | Nav, footer, avatars, author lists |
| `tagline`, `headline` | Hero pill and `<h1>` |
| `status` | Comment bubble in the contact section |
| `email`, `linkedin` | Contact buttons and footer |
| `hero.code_file`, `hero.code_lines` | Floating code card |
| `hero.figure_caption`, `hero.figure_bars` | Figure card (bars in percent, reused on academic teasers) |
| `hero.comment` | `{year, text, track}` hero comment |
| `hero.cursors` | `[{label, track}]`: first on the figure card, second on the code card |
| `hero.tools` | [Tabler icon](https://tabler.io/icons) names without `ti-` |
| `services` | "What I do" cards: `{icon, title, text, track}` |
| `experience` | `{year, text}`, newest first |
| `organizations` | Row of names under the experience list |
| `skill_aliases` | Extra terms per skill for recruiter mode, e.g. `Kubernetes: [k8s]`. Every key must be a skill used by a project (a test checks this). |

`track` is always `academic`, `professional` or `neutral`.
