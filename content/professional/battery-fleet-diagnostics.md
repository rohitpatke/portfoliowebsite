---
title: Battery fleet diagnostics in Snowflake
summary: Wrote SQL investigations against the analytics warehouse that told breaker trips from network drops, traced synchronized outages to shared wiring, and reconciled battery counts across three systems for 544 locations.
problem: With about 1,600 behind-the-meter batteries at about 270 NYC buildings, an offline unit used to mean a site visit to find out why. Battery counts also disagreed between Asana, Notion and the platform, which left some units unbillable and undispatchable.
timeline: 2026-08 to 2026-10
skills: [SQL, Snowflake, Metabase, Data Analysis, Root Cause Analysis, Data Quality, Battery Storage, Excel]

role: Field Implementation Co-Lead and Data Contributor
team: Battery program and Supplier Engineering
org: David Energy

decisions:
  - id: voltage-classification
    question: How do you tell a tripped breaker from a lost connection without a truck roll?
    options: [Send a technician to every dark site, Classify outages from the last grid-voltage reading]
    chose: Classify outages from the last grid-voltage reading
    why: A last reading of 0 V means the circuit lost power, and 120 V means it still had power but dropped off the network. Sorting about 20 dark sites this way told the team which needed an electrician and which needed Wi-Fi work, and exposed a shared network fault at two adjacent sites.
    bubble: Used the last voltage reading to tell breaker trips from Wi-Fi drops.
  - id: check-the-label
    question: Should the reconciliation trust the Asana "Batteries At Location" field?
    options: [Use the field as the source of truth, Audit the field against the platform first]
    chose: Audit the field against the platform first
    why: The field was filled on only 142 of 544 cards (545 units against 1,596 on the platform). Auditing also surfaced a shared Metabase card that compared a lowercase field name case-sensitively and returned nulls.

outcomes:
  - metric: Locations reconciled
    value: 544
  - metric: Locations with unregistered units found
    value: 24
  - metric: Duplicate serials explained
    value: "64 (4 real)"
featured: true
order: 1
---

## Investigations

- **Synchronized drops at one restaurant site:** 11 of 29 units offline. Interval and history data showed three trios dropping within two seconds of each other, twice in one morning, all idle at kitchen opening. That ruled out independent GFCI trips and pointed to shared branch breakers or daisy-chained GFCIs. Three more units were online but not charging, meaning their outlets weren't delivering power. The next visit went out with a wiring checklist instead of a reset list.
- **Wi-Fi flapping:** a second site with every unit online still showed 4 to 11 drops per unit per day.
- **Duplicate serials:** 64 duplicated serial numbers in the staging table. 4 were real double registrations and 60 were harmless re-onboardings. I also found 18 units with null serials and one placeholder serial, and handed back the SQL with a live-fleet filter.
- **Recommended versus installed:** a multi-tab workbook across 544 locations and 186 clients. 89 of 105 double-filled rows matched exactly, and 24 locations showed units in Asana that the platform had no record of.

## Techniques

Snowflake CTEs, `LISTAGG`, `MAX_BY` and semi-structured JSON paths, run through Metabase saved questions, with the SQL returned alongside each answer so the next person can rerun it.
