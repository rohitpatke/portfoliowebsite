---
# PLACEHOLDER: an example academic project. Replace it with your own work.
title: Few-shot entity recognition for clinical notes
summary: A label-efficient method that matches fully supervised entity recognition on clinical notes using 10% of the annotations.
problem: Hospitals cannot share patient notes, so every site has to annotate its own data, and clinician annotation time is slow and expensive.
timeline: 2023-09 to 2024-06
venue: Placeholder Workshop on Clinical NLP 2024
authors: [A. Coauthor, Your Name, B. Advisor]
role: Shared first author
skills: [Python, PyTorch, NLP, Statistics]
links:
  PDF: https://example.com/papers/clinical-ner.pdf
  Code: https://github.com/your-handle/clinical-ner
  Slides: https://example.com/slides/clinical-ner
decisions:
  - id: error-analysis-first
    question: Where should the first month go, into the architecture or into understanding the errors?
    options: [Tune the architecture, Error analysis on the baseline]
    chose: Error analysis on the baseline
    why: Two thirds of baseline errors came from ambiguous abbreviations, which no architecture change would fix. That finding shaped the whole method.
    bubble: Spent a month on error analysis before touching the model.
  - id: small-encoder
    question: Which encoder should the method build on?
    options: [Large general-domain model, Small clinical-domain model]
    chose: Small clinical-domain model
    why: Partner hospitals run inference on CPU-only machines inside their own network. The small model ran nine times faster for a 0.4 point F1 cost.
outcomes:
  - metric: F1 with 10% of labels
    value: 87.1
  - metric: Annotation hours saved
    value: ~120 h
featured: true
order: 10
---

## Approach

We pre-train on unlabelled notes from each site, then fine-tune with a small, actively
selected set of annotations. An abbreviation-expansion step runs before tagging, which
removes the largest class of baseline errors.

## Evaluation

Three hospital datasets, five random seeds each, compared against a fully supervised
baseline trained on all available labels. We report macro-F1 with bootstrap confidence
intervals.

## What I would do differently

Start the annotation guidelines with the clinicians, not after the first round of
disagreements. Inter-annotator agreement jumped once we did.
