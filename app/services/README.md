# app/services/

Plain Python with no HTTP code.

| File | Role |
|---|---|
| `content.py` | `ContentRepository`: loads `content/site.yaml` and every project file once, validates them, and serves them sorted (`all`, `by_type`, `featured`, `get`). Also builds the recruiter-mode JSON (`match_records`) using `skill_aliases`. `get_content()` returns the app's repository. |
| `chunking.py` | `project_to_chunks()`: splits a project into summary, problem, per-decision, outcomes and body chunks for the future AI features. Each chunk's `anchor` is an element id on the detail page, so answers can link to their source (a test checks every anchor exists). |
| `retrieval.py` | `Retriever` protocol and `FullContextRetriever` (returns every chunk). Not used yet; swap in an embedding retriever later without touching routes. |
