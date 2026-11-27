---
title: Unblocking a 61-store thermostat rollout on a corporate network
summary: Served as technical escalation for a quick-service franchisee self-installing smart thermostats across 61+ New York stores, diagnosed why devices kept failing to join the franchisor's MAC-authenticated network, and set a dispatch gate with its network engineers.
problem: Thermostats installed by the client's HVAC vendor repeatedly failed to join the franchisor's IoT Wi-Fi, which uses MAC-based authentication across about 3,500 stores, so technicians kept driving to stores to retry.
timeline: 2026-06 to 2026-08
skills: [Smart Thermostats, IoT, Network Troubleshooting, Vendor Management, Technical Writing]

role: Thermostat technical escalation point
team: Thermostat operations, with the client's HVAC vendor and the franchisor's network engineering
org: David Energy

decisions:
  - id: dispatch-gate
    question: How should technicians be dispatched while joins were failing?
    options: [Keep dispatching store by store and retry on site, Hold dispatch until each MAC is confirmed live]
    chose: Hold dispatch until each MAC is confirmed live
    why: The failures came from allow-list updates that were queued but not pushed live, and from MAC mismatches between submitted and installed units. No technician goes to the next store until network engineering confirms the MAC is live, which protects the vendor's time and keeps the client's IT accountable.
    bubble: Stopped wasted drives by gating dispatch on network confirmation.

outcomes:
  - metric: Stores in the rollout
    value: 61+
---

## What I sent

Correspondence to the franchisor's network engineers asking for a log check, live confirmation and a MAC match before the next dispatch.
