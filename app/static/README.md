# app/static/

Front-end assets served as-is (no build step).

## css/

Loaded in this order by `base.html`:

| File | Contents |
|---|---|
| `tokens.css` | Every colour, font, size, radius and duration as a custom property. Light theme in `:root`, dark theme under `prefers-color-scheme: dark`. |
| `base.css` | Reset, typography, prose, layout helpers |
| `components.css` | Reusable pieces: buttons, cards, comment, cursor, metrics, decisions, forms |
| `sections.css` | Page regions: hero, homepage sections, detail layouts |
| `motion.css` | Hover lift, hero drift, scroll-reveal states, view transitions |

**Track colours.** `.track--academic` (violet), `.track--professional` (teal) and
`.track--neutral` (gray) set `--track`, `--track-soft` and `--track-line`; components only
read those. Recolour a track via `--color-academic*` / `--color-professional*` (plus their
dark and `--inverse-*` versions). `.inverse` flips the palette inside an element (used by
the research band). Keep text at 4.5:1 contrast.

## js/

All ES modules.

| File | Role |
|---|---|
| `motion.js` | Scroll reveal for `[data-animate]` and the lazy loader for `[data-effect]` modules in `effects/` |
| `filters.js` | Homepage filter pills (All / Research / Professional) |
| `recruiter.js` | Recruiter mode: keyword-matches a pasted job description against project skills and `skill_aliases`, entirely in the browser |
| `effects/` | Optional heavy animations (none yet); see `effects/README.md` |

All motion respects `prefers-reduced-motion`. Content is only hidden under the `.js` class,
which an inline script in `base.html` removes if `motion.js` hasn't started within 3 s.

## img/, lottie/

Favicon and images; Lottie JSON files for effects (empty).
