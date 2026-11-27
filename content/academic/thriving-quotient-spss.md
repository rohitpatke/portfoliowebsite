---
title: What predicts student thriving? A survey analysis in SPSS
summary: Used correlation and multiple regression in SPSS to test how sense of community, spirituality and institutional integrity relate to undergraduates' Thriving Quotient scores.
problem: Universities want to know which parts of campus life they can influence to help students thrive and stay, but survey scales overlap, so the unique contribution of each one is unclear.
timeline: 2026-07 to 2026-07
skills: [SPSS, Statistics, Multiple Regression, Correlation Analysis, Survey Analysis, Quantitative Research, APA Reporting]

venue: EDD771 Quantitative Data Analysis, Judson University
authors: [Rohit Patke]
role: Sole author

decisions:
  - id: multiple-regression
    question: How should the combined effect of the three predictors be tested?
    options: [Three separate correlations only, Standard multiple linear regression]
    chose: Standard multiple linear regression
    why: Regression gives an overall model fit for the combined question and separates each predictor's unique variance from shared variance while controlling for the other two.
  - id: check-normality
    question: Spirituality was negatively skewed. Is the Pearson result still trustworthy?
    options: [Report Pearson as is, Confirm with a non-parametric test]
    chose: Confirm with a non-parametric test
    why: Spearman's rho (ρ = .48, p < .001) reached the same conclusion, so the skew didn't distort the result.

outcomes:
  - metric: Sense of community vs thriving
    value: r = .64 (41% of variance)
  - metric: Students in sample
    value: 156
---

## Data

The Fall 2024 Thriving Quotient survey: 33 variables for 156 traditional undergraduates. It covers the overall TQ score, five sub-scales, three influencing scales, seven outcomes and 17 background variables.

## Results

- Sense of community: r(150) = .64, p < .001
- Spirituality: r(150) = .42, p < .001
- Institutional integrity: r(150) = .39, p < .001

Sense of community was the strongest predictor of thriving.

## Limitations

The sample comes from a single institution, and spirituality was not normally distributed.
