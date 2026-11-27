---
title: "TinyML Thermostat: on-device machine learning for comfort and energy efficiency"
summary: Trained, quantized and benchmarked a thermostat model that fits in 0.53 KB on an ESP32. Driving a predictive controller, it held 94% comfort against 58% for a reactive thermostat.
problem: Fixed-schedule thermostats can't adapt to weather or occupancy, and smart thermostats lose their optimization when Wi-Fi drops because the logic lives in the cloud. Homes, restaurants and gyms need control that runs on the cheap microcontroller already in the box.
timeline: 2024-01 to 2026-07
skills: [Python, Machine Learning, TinyML, TensorFlow Lite, Model Quantization, Model Predictive Control, Embedded Systems, ESP32, Scikit-learn, Data Analysis, Research]

venue: Ed.D. in Computer Science capstone, Judson University, 2026
authors: [Rohit Patke]
role: Sole author

decisions:
  - id: public-dataset
    question: Where should the training data come from?
    options: [Instrument a building and collect my own data, Use a public residential HEMS dataset]
    chose: Use a public residential HEMS dataset
    why: The Kaggle Residential HEMS dataset has 47,040 half-hour rows with every HVAC variable needed (indoor and outdoor temperature, occupancy, setpoint, HVAC energy). That made the work reproducible and avoided human-subjects review.
    bubble: Picked a public dataset so anyone can rerun the whole pipeline.
  - id: mlp-over-forest
    question: Which model should ship to the microcontroller?
    options: [Random Forest, Small MLP (16 and 8 units)]
    chose: Small MLP (16 and 8 units)
    why: Random Forest had the lowest MAE (0.024 °C) but weighed about 8.8 MB, far beyond the ESP32's memory. The small MLP matched it (MAE 0.028 °C, best R² of 0.9994) at 2.13 KB, and 0.53 KB after 8-bit quantization.
  - id: control-over-accuracy
    question: What should the evaluation optimize for after the models were all above R² 0.999?
    options: [Squeeze out more predictive accuracy, Compare control strategies in simulation]
    chose: Compare control strategies in simulation
    why: Every nonlinear model was already accurate enough. A fitted forward thermal model let me run a predictive controller against four baselines, which showed that the control strategy matters more than the last decimal of accuracy.

outcomes:
  - metric: Comfort, ML-predictive controller
    value: 94.3%
  - metric: Comfort gain over reactive thermostat
    value: +36.1 pp
  - metric: Model size after 8-bit quantization
    value: 0.53 KB
  - metric: Extra energy versus reactive baseline
    value: +7.95%

featured: true
order: 1
---

## How it developed

| Stage | When | What |
|---|---|---|
| Literature review | Spring 2024 | EDD715 review of machine learning for thermostat optimization |
| Prospectus | Aug 2024 | First framing of the TinyML thermostat question |
| Proposal | Spring 2025 | Research questions, design and data plan |
| Drafts | Apr–Jul 2026 | Training, conversion, simulation and write-up |
| Final submission and defense | Jul 2026 | Dissertation, recorded defense, slide deck and code appendix |

## Research questions

1. Can tiny models trained on public data be converted for real-time HVAC control on microcontroller-class hardware?
2. What predictive accuracy, simulated energy savings and comfort gains can they achieve?
3. What practical problems come up when training, converting and benchmarking them?

## Approach

- **Data:** the Residential HEMS dataset (47,040 half-hour observations, about two years and nine months) with a strict time-based split.
- **Models:** Linear Regression, Random Forest, Gradient Boosting and a small multi-layer perceptron, compared on accuracy and on whether they fit the memory budget.
- **Deployment target:** an ESP32 with a DHT11 temperature and humidity sensor. Inference runs orders of magnitude faster than the half-hour control cycle.
- **Simulation:** a forward thermal model fitted on the training segment drove a single-step model predictive controller across a 4,704-step test segment covering all twelve months. Baselines were no HVAC, a fixed schedule, the dataset's actual policy and a reactive thermostat.

## Results

| Strategy | Comfort | Energy |
|---|---|---|
| No HVAC | 9.7% | 0 kWh |
| Fixed schedule | 20.8% | 2,834 kWh |
| Dataset's actual policy | 60.2% | 1,668 kWh |
| Reactive thermostat | 58.2% | 1,805 kWh |
| **ML-predictive controller** | **94.3%** | **1,949 kWh** |

The predictive controller beat the fixed schedule on both comfort and energy. The comfort gain over the reactive thermostat held across all four seasons and several deadband settings, and was largest in winter (+51.5 pp) and spring (+39.6 pp).

A follow-up model inferred the occupant's setpoint from outdoor conditions, forecast trend, occupancy and time alone, to within 0.27 °C. Running fully on its own with no setpoint input, the controller still reached 79% comfort, and 95% with a tighter deadband.

## What I'd do differently

The energy effect over the reactive baseline is smaller than field studies report, which is expected from a simulation. The next step is to replicate the controller on a real ESP32 in an occupied building and measure it against metered data.
