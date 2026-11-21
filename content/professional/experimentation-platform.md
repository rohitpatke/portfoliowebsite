---
# PLACEHOLDER: an example professional project. Replace it with your own work.
title: Self-serve experimentation platform
summary: A metrics layer and readout tool that let product teams run and read A/B tests without waiting for an analyst.
problem: Every experiment readout was a hand-written notebook. Analysts were the bottleneck, and two teams once reached opposite conclusions from the same test.
timeline: 2023-06 to 2023-12
role: Data Engineering Intern
team: Growth Analytics, 3 people
org: Acme Analytics
skills: [Python, SQL, A/B Testing, Statistics, Airflow]
links:
  Demo: https://example.com/demo/experiments
decisions:
  - id: metrics-as-code
    question: How should metric definitions be shared?
    options: [Shared notebook templates, Versioned metric definitions in SQL]
    chose: Versioned metric definitions in SQL
    why: One reviewed definition per metric ended the "which conversion rate?" debates and made every readout reproducible.
    bubble: Put metric definitions in version control so every team computes them the same way.
  - id: sequential-testing
    question: How do we stop people from peeking at results early?
    options: [Fixed-horizon tests with a warning, Sequential testing]
    chose: Sequential testing
    why: People were going to peek anyway. Sequential tests make early looks statistically valid instead of forbidding them.
outcomes:
  - metric: Time to readout
    value: 5 days → 1 day
  - metric: Experiments per quarter
    value: 3×
featured: true
order: 20
---

## Context

Product teams wanted to test more ideas, but each readout took an analyst most of a
week. The definitions behind each metric lived in personal notebooks and drifted apart.

## What I built

A small library of reviewed metric definitions, a nightly Airflow job that computes them
per experiment, and a readout page that shows effect sizes with sequential confidence
intervals.

## What I learned

Statistical rigour only sticks when the rigorous path is also the easy one.
