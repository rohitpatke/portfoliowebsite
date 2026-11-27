---
# TODO: in progress as of Oct 2026. Update with what shipped and the final savings figures.
title: Demand-charge credit tooling for battery customers
summary: Assigned to build the software that shows battery customers the demand-charge savings their batteries create, covering a data-quality-gated ingest, a counterfactual peak model, a credit engine, payout logic and guardrail metrics.
problem: Batteries shave demand peaks and cut customers' Con Edison delivery charges, but customers never saw that saving. The company was also paying Ramp credits that partly duplicated it (forecast at 35.55% of installed capacity against 15.5% realized).
timeline: 2026-10 to 2026-10
skills: [Python, SQL, dbt, Counterfactual Modeling, Utility Billing, Data Quality, Technical Specification]

role: Data and Software Contributor
team: Supplier Engineering, with Risk and Data
org: David Energy

decisions:
  - id: gate-the-ingest
    question: Which billing cycles should feed the credit calculation?
    options: [Every cycle on record, Only cycles that pass data-quality gates]
    chose: Only cycles that pass data-quality gates
    why: Credits should only be computed from actual meter reads with at least 80% counterfactual coverage, excluding grid-event days, so a bad cycle can't produce a bad credit.
    bubble: Put data-quality gates in front of the money.
  - id: open-questions-first
    question: How should unresolved definitions be handled?
    options: [Assume values and build, List them for Risk and Data to resolve]
    chose: List them for Risk and Data to resolve
    why: Five questions (grid-event calendar, sign convention, cycle window edges, supply dollar base and enum values) changed the numbers, so I listed them rather than guessing.

outcomes:
  - metric: DCM value, Sep 2026 baseline
    value: "~$4k/month"
  - metric: Savings potential, Sep 2026 baseline
    value: "~$6k/month"
---

## Scope

- A per-cycle ingest table with data-quality gates.
- A counterfactual peak model, using metered load plus battery discharge priced at the delivery demand rate.
- A credit engine mirroring the Supply product: a 2% supply discount, a DCM credit, and a top-up to a 3% cohort target capped at 3.5% per bill.
- Revised Ramp payout logic and three new savings-email line items.
- Guardrail metrics, including credits under $4.80 per MWh.

## Delivered so far

The ingest-stage design, pseudocode for the eligibility gates, and the dbt tests to add.
