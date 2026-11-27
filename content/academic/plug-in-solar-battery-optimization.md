---
title: Battery optimization for Utah plug-in solar (HB 340)
summary: Built a two-layer system that forecasts next-day solar output and solves a linear program for battery dispatch under Utah HB 340's no-export rule. Self-consumption rose from 55% to 87% and grid costs fell by about 26%.
problem: Utah HB 340 (2025) lets renters and homeowners plug in up to 1,200 W of solar without an interconnection agreement, but it bans grid export. Solar peaks at noon while household load peaks morning and evening, so 30 to 45% of a summer day's output can go to waste.
timeline: 2026-03 to 2026-05
skills: [Python, Machine Learning, Gradient Boosting, Linear Programming, Optimization, Time Series Forecasting, pvlib, Solar PV, Battery Storage, Feature Engineering, AWS Open Data]

venue: DCS615 Foundations of Machine Learning, Judson University
authors: [Rohit Patke]
role: Sole author

decisions:
  - id: lp-over-rules
    question: How should the battery decide when to charge and discharge?
    options: [Fixed schedule (charge at noon and discharge at 6 pm), Linear program on a 24-hour forecast]
    chose: Linear program on a 24-hour forecast
    why: A fixed rule misses the solar peak on cloudy days. Re-solving the LP each day against forecast solar, forecast load and Rocky Mountain Power's time-of-use rates, with no-export as a hard constraint, saved $180 a year more than the fixed schedule.
    bubble: Made no-export a hard constraint in the optimizer, not an afterthought.
  - id: physics-guided
    question: How should physically impossible forecasts be handled?
    options: [Trust the raw model output, Clip to the pvlib clear-sky envelope]
    chose: Clip to the pvlib clear-sky envelope
    why: Raw models sometimes predicted irradiance above the clear-sky maximum, which would make the optimizer schedule charging from energy that doesn't exist. Bounding the clearness index cut MAE by 1.8% at no compute cost.

outcomes:
  - metric: Self-consumption
    value: 55% → 87%
  - metric: Annual grid cost reduction
    value: ~26% ($310/yr)
  - metric: Solar forecast skill vs persistence
    value: 0.966
  - metric: Battery payback
    value: 5–7 yrs (from 11)
featured: true
order: 5
---

## Data

- **NREL NSRDB v3:** 2019 half-hourly irradiance and weather for Salt Lake City (17,520 intervals), from the AWS Open Data Registry.
- **DOE OEDI ResStock:** simulated load profiles for Utah single-family homes in climate zone 5B, resampled to 30 minutes.

## Approach

- **Layer 1, forecasting:** Gradient Boosting models for 24-hour solar and load, using 14 engineered features (cyclical time encodings, clearness index, solar zenith, time-of-use flags, STL residuals). The pipeline was built to swap in an LSTM later. Data was split by time, January to October for training and November to December for testing.
- **Layer 2, dispatch:** a linear program (SciPy HiGHS) minimizing grid import cost over 48 half-hour steps, with a 1.5 kWh battery, a 1.2 kW power cap, 94% round-trip efficiency and no export.

## Results

| | No battery | Fixed schedule | LP optimized |
|---|---|---|---|
| Annual grid cost | ~$1,180 | ~$1,050 | ~$870 |
| Self-consumption | ~55% | ~68% | ~87% |
| CO₂ avoided per year | 0 kg | ~190 kg | ~520 kg |
| Payback | n/a | ~11 years | 5–7 years |

A climate stress test (2050 deltas consistent with NREL Sup3rCC) suggested the optimizer's advantage over fixed dispatch grows by about 12 to 18%.

## What I'd do differently

Model battery degradation (about 2% capacity loss a year), use a distribution of household load profiles instead of one, and try a reinforcement-learning dispatcher once the LP baseline is trusted.
