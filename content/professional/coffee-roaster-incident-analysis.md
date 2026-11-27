---
title: Separating evidence from claims in a customer equipment dispute
summary: When a coffee customer blamed a failed roaster fan on battery installation work, I assembled the evidence and showed that the planned power disruption and the fan failure were two separate events.
problem: A customer attributed a failed roaster fan to electrical work at a site scoped for load combining with a disclosed disruption of up to 20 minutes. The account team needed a position they could defend.
timeline: 2026-08 to 2026-09
skills: [Root Cause Analysis, Battery Storage, Electrical Troubleshooting, Technical Writing, Customer Communication]

role: Customer Success Engineer, Energy and Systems (battery field implementation co-lead)
team: Battery program and account team
org: David Energy

decisions:
  - id: split-the-claims
    question: How should the dispute be answered?
    options: [Defend the install as a whole, Separate the power loss from the fan failure]
    chose: Separate the power loss from the fan failure
    why: The brief power loss was real, planned and disclosed. The fan failure was mechanical and independent. There was no scorching and no blown fuses or tripped breakers, the grid-following inverter is capped at 640 W and cannot push an overvoltage, the circuits were dedicated, and both electricians agreed.
    bubble: Pulled apart two claims that were being treated as one.
  - id: name-the-gap
    question: Should the write-up mention the weak point in the company's position?
    options: [Leave it out, Name it and recommend a fix]
    chose: Name it and recommend a fix
    why: The denial rested on verbal attestation with no breaker log. Saying so, and recommending that panel work be documented precisely, gave the account team the one thing they still needed.
---

## Evidence assembled

Slack threads, the customer's emails, the EcoFlow specifications and the internal install standard.
