---
# PLACEHOLDER: an example academic project. Replace it with your own work.
title: How well calibrated are probabilistic demand forecasts?
summary: An MSc thesis measuring the calibration of six forecasting models across 40 retail datasets, plus a cheap post-hoc fix.
problem: Planning teams act on forecast intervals as if they were reliable, but nobody had checked whether a 90% interval really contains 90% of outcomes.
timeline: 2022-10 to 2023-08
venue: MSc thesis, Placeholder University
authors: [Your Name]
skills: [Python, Statistics, Machine Learning, SQL]
links:
  PDF: https://example.com/papers/forecast-calibration.pdf
  Code: https://github.com/your-handle/forecast-calibration
decisions:
  - id: coverage-over-crps
    question: Which metric should headline the results?
    options: [CRPS, Interval coverage, Pinball loss]
    chose: Interval coverage
    why: Planners read intervals, not CRPS. Reporting coverage made the gap concrete, as in "your 90% interval holds 71% of the time".
    bubble: Reported coverage instead of CRPS, because that is what planners read.
  - id: conformal-fix
    question: How should the miscalibration be fixed?
    options: [Retrain with a new loss, Post-hoc conformal adjustment]
    chose: Post-hoc conformal adjustment
    why: It works on top of any existing model, so teams can adopt it without retraining their production forecasts.
outcomes:
  - metric: Coverage of 90% intervals
    value: 71% → 89%
  - metric: Datasets evaluated
    value: 40
featured: true
order: 20
---

## Method

Each model produced 90% prediction intervals on a rolling-origin backtest. Coverage was
measured per series and summarised with the median and interquartile range, so a few
easy series could not hide the rest.

## Findings

Every model was overconfident on intermittent, low-volume products. A split-conformal
adjustment, fitted on the most recent eight weeks, brought median coverage to 89% while
widening intervals by only 12%.
