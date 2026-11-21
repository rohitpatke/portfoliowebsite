# app/templates/

Jinja templates. Every template gets `site` and `features` from the context processor.

| Folder | Contents |
|---|---|
| `base.html` | Page shell: fonts, icons, stylesheets, nav, footer, `motion.js` |
| `main/` | `index.html` (includes the homepage sections) and `404.html` |
| `sections/` | One file per homepage section: hero, services, projects, research band, experience, contact (with recruiter mode) |
| `projects/` | `list.html`, `academic.html` (paper layout), `professional.html` (case study) |
| `components/` | Macros. `cards.html`: project, service, publication, decision cards, metric tiles, link chips. `workspace.html`: avatar, cursor, comment bubble. Import with `{% import "components/cards.html" as cards with context %}`. |
| `partials/` | `nav.html`, `footer.html`, `chat_widget.html` (only when `ENABLE_CHAT`) |

Conventions:

- Exactly one `<h1>` per page (a test checks this); `h2` per section, `h3` inside.
- Detail-page section ids (`summary`, `problem`, `decisions`, `outcomes`, `details`) and
  decision ids are the chunk anchors from `services/chunking.py`.
- Add `data-animate` (and `style="--delay: N"` for staggering) to reveal on scroll.

## Adding a homepage section

1. Create `sections/home_<name>.html` with
   `<section class="section" id="<name>" aria-labelledby="<name>-title">`.
2. Put its data in `site.yaml` (add the key to `SITE_REQUIRED_KEYS` in
   `services/content.py` if required) or pass it from `blueprints/main.py`.
3. Include it in `main/index.html` and add styles to `static/css/sections.css`.
