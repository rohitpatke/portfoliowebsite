---
# PLACEHOLDER: an example professional project. Replace it with your own work.
title: Real-time fraud scoring service
summary: Replaced a nightly batch fraud model with a streaming scoring service that decides inside the checkout request.
problem: Fraud was detected the morning after a purchase, once goods had shipped. The business needed a decision within the 100 ms checkout budget.
timeline: 2025-01 to 2025-09
role: ML Engineer
team: Risk Platform, 5 engineers
org: Example Payments
skills: [Python, Machine Learning, Kafka, Kubernetes, SQL]
links:
  Write-up: https://example.com/blog/realtime-fraud
decisions:
  - id: streaming-features
    question: Where should real-time features be computed?
    options: [In the request path, In a streaming feature store]
    chose: In a streaming feature store
    why: Aggregating 30 days of history inside the request blew the latency budget at p95. Precomputing features from the event stream kept scoring under 40 ms.
    bubble: Moved feature computation out of the request path to keep p95 under 40 ms.
  - id: shadow-launch
    question: How do we launch without risking false declines?
    options: [Direct cutover, Shadow mode for four weeks, A/B test on 5% of traffic]
    chose: Shadow mode for four weeks
    why: Shadow scoring compared decisions with the batch model on real traffic, with no customer impact, before blocking was switched on.
  - id: boosted-trees
    question: Which model family should we serve?
    options: [Gradient-boosted trees, Deep sequence model]
    chose: Gradient-boosted trees
    why: Similar recall at a tenth of the serving cost, plus per-feature explanations that the disputes team needed.
outcomes:
  - metric: p95 scoring latency
    value: 38 ms
  - metric: Fraud losses
    value: −18%
  - metric: False declines
    value: −9%
featured: true
order: 10
---

## Context

The batch model was accurate but late: by the time it flagged an order, the order had
shipped. Moving to real time meant meeting a hard latency budget without losing the
accuracy the risk team trusted.

## Architecture

Checkout events stream into a feature pipeline that keeps rolling aggregates per card,
device and merchant. The scoring service reads precomputed features, runs the model and
returns a decision with the top contributing features attached.

## What I learned

Agreeing on the launch criteria with the risk team before writing code saved weeks of
debate at the end. Shadow mode turned "do we trust it?" into a dashboard.
