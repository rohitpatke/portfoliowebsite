---
title: Python thermostat insights and a schedule data model
summary: Taught myself Python to turn thermostat history into client-facing optimization reports, then co-designed a schedule-event table with engineering.
problem: Thermostat insights for clients were assembled by hand, and schedule changes weren't captured as structured events the product could build on.
timeline: 2024-10 to 2025-07
skills: [Python, Data Analysis, Data Modeling, Smart Thermostats, Automation]

role: Thermostat Operations and Implementation Specialist
team: Thermostat operations, with engineering
org: David Energy

decisions:
  - id: script-the-report
    question: How should client insights reports be produced?
    options: [Keep compiling them by hand, Script them in Python]
    chose: Script them in Python
    why: Scripts written on top of a full field schedule made the report repeatable, and led to the data-model work and later engineering assignments.
    bubble: Learned Python because the report kept getting built by hand.

outcomes:
  - metric: Scripts written
    value: 5
---

## Scripts

Insights Report Generator V1 and V2, a recommendations script, an audit-issues script, and a before-versus-after programming analysis of thermostat history. Together they produced a client insights report in July 2025.

## Data model

In June 2025 I co-designed a thermostat schedule-event-change table with an engineer, with fields for thermostat_id, day_of_week, event_label, heat and cool set points, time_of_day and created_at.
