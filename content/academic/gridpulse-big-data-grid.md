---
title: "GridPulse: a big data platform for grid forecasting and reliability"
summary: Designed a streaming lakehouse that joins smart meter, weather, market, sensor and renewable data so one feature layer serves demand forecasting, curtailment reduction, equipment health and outage risk.
problem: Utilities already run about 119 million US smart meters, yet California curtailed 3.4 million MWh of wind and solar in 2024 and outages cost US customers around $121 billion. The data sits in billing, alarm and reporting systems that were never built to be joined.
timeline: 2026-05 to 2026-07
skills: [Big Data, Data Architecture, Data Engineering, Kafka, Apache Flink, Apache Spark, Delta Lake, Feature Store, Machine Learning, Energy Analytics, Data Privacy]

venue: DCS532 Big Data Technologies and Tools, Judson University
authors: [Rohit Patke]
role: Sole author

decisions:
  - id: one-feature-layer
    question: Should forecasting, curtailment, equipment health and reliability be separate products?
    options: [Four separate products, One platform on a shared feature layer]
    chose: One platform on a shared feature layer
    why: The problems are linked. Transformer aging depends on the load forecast, curtailment depends on load and renewable forecasts, and blackout risk depends on both plus equipment condition. Separate products can't see those links.
    bubble: Put four grid models on one feature layer because their problems are linked.
  - id: as-of-weather
    question: Which weather values should train the models?
    options: [Observed weather, The forecast available at the time]
    chose: The forecast available at the time
    why: Training on weather that was observed later leaks the future. The model tests well and then falls apart in production.
  - id: privacy-in-pipeline
    question: Where should smart meter privacy be enforced?
    options: [In a policy document, In the pipeline itself]
    chose: In the pipeline itself
    why: Interval data reveals when a household wakes, cooks and leaves. Pseudonymizing at ingest, setting a 15-premise minimum on analytics queries, and federated learning with noise make privacy a property of the system, not a promise.
---

## Architecture

- **Ingest:** Kafka for anything faster than an hourly cadence, with scheduled pulls for weather and prices. A data contract (schema, freshness, units) is checked at ingest.
- **Processing:** Flink on event time, because meter clocks drift and packets arrive late.
- **Storage and training:** Delta Lake or Iceberg on object storage; Spark and Ray for training; Feast keeps training and serving features identical.
- **Models:** LightGBM baselines, Temporal Fusion Transformer forecasts, survival models and graph neural networks for equipment health, autoencoders for anomalies. Every forecast is a calibrated range, not a single number.

## Modules and targets

1. Demand forecasting from 15 minutes to 7 days, down to the transformer (target 2% day-ahead error at system level).
2. Renewable forecasting feeding a storage dispatch optimizer (target 15% less curtailment).
3. Equipment health as a ranked work list (target two weeks of warning).
4. Reliability monitoring using last-gasp meter messages for fault location.

## Ethics and fairness

Forecast error, alert coverage and restoration time are reported by income decile every cycle. Where fairness costs money, that tradeoff goes to the regulator instead of being buried in an objective function.

## Other course work

- A data pipeline assignment covering ingestion, storage and processing.
- A recorded video, *Big Data in the Energy Sector*.
