---
title: "Nike on Reddit: sentiment versus stock price"
summary: Scraped 13 years of Nike discussion from five subreddits, scored it with three sentiment lexicons, and compared the daily sentiment with Nike's share price.
problem: Investors and brand teams want to know how the public feels about a company in time to act, but reading thousands of posts by hand is too slow, and general-purpose sentiment tools misread finance language.
timeline: 2025-06 to 2025-07
skills: [Python, NLP, Sentiment Analysis, Web Scraping, Reddit API, VADER, Data Cleaning, Data Visualization, Pandas]

venue: DCS702 Analytic Thinking and Statistics in Research, Judson University
authors: [Rohit Patke]
role: Sole author

decisions:
  - id: reddit-over-twitter
    question: Which platform should supply the posts?
    options: [Twitter (X), Reddit]
    chose: Reddit
    why: Both have engaged users and APIs, but Twitter's data sits behind a paid tier. Reddit's free API (through PRAW) also gives longer, more candid posts.
  - id: finance-lexicon
    question: Which sentiment dictionary should score finance discussion?
    options: [General-purpose lexicon only, Add the Loughran-McDonald finance lexicon]
    chose: Add the Loughran-McDonald finance lexicon
    why: Words like "risk" or "liability" are neutral in everyday speech but negative in finance. I ran Loughran-McDonald alongside VADER, and the NRC emotion lexicon for the emotion profile.
    bubble: Scored finance talk with a finance dictionary, not a general one.

outcomes:
  - metric: Years of posts analyzed
    value: 2011–2024
  - metric: Subreddits scraped
    value: 5
---

## Approach

1. **Scrape** posts mentioning Nike from r/investing, r/shoes, r/finance, r/stocks and r/running using PRAW, saved to CSV.
2. **Clean** missing values and text problems, then order by date.
3. **Score** each post with weighted word counts against the lexicons, averaging to a positive, negative or neutral label.
4. **Join** daily sentiment with Nike's stock price and chart the two together.

## Findings

- Positive posts leaned on words like *growth*, *revenue*, *earnings* and *long-term*; negative posts on *recession*, *tariff*, *COVID*, *delay* and *decline*.
- Polarity swung between positive and negative over the years but stayed net positive overall.
- The NRC emotion radar showed high *trust* and *anticipation* and low anger, sadness, fear and disgust.
