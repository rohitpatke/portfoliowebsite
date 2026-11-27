---
title: Automated battery proposals V3
summary: Scoped the third version of the battery proposal generator end to end, tracing each new Notion field through the generator code into the internal and client Google Doc templates.
problem: Battery proposals are generated from Notion "Battery Placement Options" records into a Google Doc template, but the placement data didn't carry Wi-Fi signal strength, install difficulty or rack sizing into the proposals.
timeline: 2026-08 to 2026-09
skills: [Python, Technical Specification, Notion, Google Docs, Automation, Flask, Docker, PostgreSQL]

role: Data and Software Contributor
team: Supplier Engineering, paired with an engineer
org: David Energy

decisions:
  - id: trace-every-field
    question: How deep should the ticket scope go?
    options: [List the new Notion fields and hand off, Trace each field through code and templates]
    chose: Trace each field through code and templates
    why: Following each property from the Notion schema through the Generate Proposal trigger mapping to the template placeholders showed which fields existed, which needed migrating (difficulty to High, Medium or Low), and which needed fallback copy when empty.
    bubble: Traced every field from Notion to the final Google Doc before sizing the ticket.
  - id: flag-dependency
    question: How should rack information be handled?
    options: [Build it into this ticket, Size it separately as a dependency]
    chose: Size it separately as a dependency
    why: Rack information depends on the 3-to-18-battery rack lookup owned by a sibling ticket. Sizing V3 at S or M depending on that kept the estimate honest, and I also flagged that two fields were outside the Q3 plan.

outcomes:
  - metric: New proposal fields scoped
    value: 4
  - metric: Estimate
    value: S/M
order: 5
---

## Fields added or changed

- Wi-Fi signal strength (new select field)
- Install difficulty (migrated to High, Medium or Low)
- Rack information, tied to the rack lookup
- Wiring type (already present, newly surfaced in the templates)

## Getting into the codebase first

In August 2026 I set up the company monorepo locally (Docker Compose Postgres, a production dump, Python and Flask) and worked through a pull request in which an unhandled SQLAlchemy integrity error on a duplicate address poisoned a session and dropped a batch of building records, and why the fix put `session.rollback()` at the point of failure. By October I was a requested reviewer on engineering pull requests.

## Status

<!-- TODO: update with what shipped. -->
In progress with engineering as of September 2026, pairing with an engineer on the Supplier Engineering sprint board.
