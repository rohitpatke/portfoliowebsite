# app/ai/

Scaffolding for two future features: a project chatbot and a job-description matcher.
The blueprint (`/api`) is registered only when `ENABLE_CHAT` or `ENABLE_JD_MATCH` is true.
Each route returns 404 when its own flag is off and 501 until it is implemented.

| File | Role |
|---|---|
| `__init__.py` | The `ai` blueprint |
| `routes.py` | `POST /api/chat`, `POST /api/jd-match` (stubs) |
| `prompts.py` | Draft system prompts with grounding and citation rules |

Related pieces elsewhere: `services/chunking.py`, `services/retrieval.py`,
`scripts/build_index.py`, `templates/partials/chat_widget.html` (disabled placeholder), and
the swap point in `findMatches()` in `static/js/recruiter.js`.

## Building the chatbot

1. Add the model SDK to `requirements.txt`; keep the API key in the host's environment.
2. At startup, build a `FullContextRetriever` from `project_to_chunks()` for every project
   and store it in `app.extensions`.
3. In `chat()`: validate `question` (string, max 500 chars), format chunks as
   `<chunk id="...">text</chunk>`, fill `CHAT_SYSTEM_PROMPT`, call the model.
4. Parse `[type/slug#anchor]` citations, drop ids that aren't real chunks, and return
   `{"answer", "sources": [{"id", "title", "url"}]}`.
5. Replace the placeholder form in `chat_widget.html` with a module that posts to
   `data-endpoint` and renders with `textContent`.

## Building the JD matcher

1. In `jd_match()`: validate `text` (20–8,000 chars), wrap it in `<job_description>` tags,
   call the model with `JD_MATCH_SYSTEM_PROMPT` and structured output.
2. Return `{"matches": [{"title", "type", "label", "url", "evidence", "matched"}]}`, taking
   `title`, `type`, `label`, `url` from your own data and only `evidence`/`matched` from the model.
3. In `recruiter.js`, replace the keyword block in `findMatches()` with the commented `fetch`;
   keep keyword matching as the fallback.

## Guardrails

- Answer only from retrieved chunks; validate citations against real chunk ids.
- Treat questions and job descriptions as data; render all output with `textContent`.
- Rate-limit `/api/*` per IP and cap input sizes on the server (`MAX_CONTENT_LENGTH`).
- Set a provider spend limit; the feature flags double as kill switches.
- Log request ids, latency and token counts, not the pasted text.
