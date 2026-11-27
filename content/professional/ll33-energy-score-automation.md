---
title: Automating LL33 energy score downloads with Selenium
summary: Wrote a Selenium script that downloads and prints Local Law 33 energy grade labels for more than 1,500 properties, saving over 40 work hours.
problem: NYC buildings must post their LL33 energy efficiency grade, and fetching each label by hand from the city portal for 1,500+ client properties was days of clicking.
timeline: 2020-09 to 2021-01
skills: [Python, Selenium, Web Scraping, Automation, NYC Local Law 33]

role: Junior Energy Auditor
org: Carleton Energy Consulting

decisions:
  - id: automate-the-portal
    question: How should 1,500+ labels be retrieved?
    options: [Split the list across staff by hand, Script the portal with Selenium]
    chose: Script the portal with Selenium
    why: The steps were identical for every property, so a browser script could loop the whole list unattended.
    bubble: Scripted a 1,500-property chore that was eating days.

outcomes:
  - metric: Properties processed
    value: 1,500+
  - metric: Work hours saved
    value: 40+
---
