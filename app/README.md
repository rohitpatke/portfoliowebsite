# app/

The Flask application package.

| File / folder | Role |
|---|---|
| `__init__.py` | `create_app(env)`: loads config and content, registers blueprints, 404 handler |
| `config.py` | Settings per environment (`development`, `production`, `testing`) and env-var feature flags |
| `models.py` | Pydantic models `Project`, `Decision`, `Outcome` with all content validation rules |
| `services/` | Content loading, chunking, retrieval |
| `blueprints/` | Page routes |
| `ai/` | Future `/api` endpoints, registered only when a flag is on |
| `templates/`, `static/` | Jinja templates and front-end assets |

## How it fits together

- `create_app` builds one `ContentRepository` and stores it in `app.extensions["content"]`.
  It is the only code that reads files; routes and templates get validated objects.
- A context processor gives every template `site` (from `site.yaml`) and `features`
  (`{"chat": bool, "jd_match": bool}`).
- The two project types, `academic` and `professional`, come from the content folder names
  and are reused everywhere: URLs, CSS classes (`track--academic`), `data-type` attributes.

## Environment variables

See `.env.example`: `APP_ENV`, `SECRET_KEY`, `ENABLE_CHAT`, `ENABLE_JD_MATCH`,
`FREEZER_BASE_URL`, `HOST`, `PORT`.
