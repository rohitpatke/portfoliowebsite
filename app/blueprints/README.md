# app/blueprints/

Page routes. Each is a few lines: fetch from `get_content()`, render a template.

| File | Routes |
|---|---|
| `main.py` | `/`: homepage (featured projects, publications, recruiter data) |
| `projects.py` | `/<kind>/` list page and `/<kind>/<slug>/` detail page, where `kind` is `academic` or `professional` (anything else is a 404). Academic detail uses `projects/academic.html` (paper layout), professional uses `projects/professional.html` (case study). |
