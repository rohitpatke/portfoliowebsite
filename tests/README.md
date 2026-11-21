# tests/

Run with `pytest` from the repository root.

| File | Checks |
|---|---|
| `test_content.py` | Every project file validates, both tracks have projects, `skill_aliases` keys are real skills, chunk ids are unique, and malformed files fail loudly |
| `test_routes.py` | All pages return 200, unknown URLs and wrong types return 404, one `<h1>` per page, chunk anchors exist on detail pages, recruiter JSON is embedded, AI routes follow their flags |
