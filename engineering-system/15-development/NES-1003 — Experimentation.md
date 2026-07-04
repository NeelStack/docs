---
document_id: NES-1003
title: Experimentation
subtitle: Enterprise Experimentation Culture, Hypotheses & Statistical Baselines
version: 1.0.0
status: Draft
classification: Internal
owner: Product Analytics Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1002 Feature Lifecycle
next_document: NES-1004 — A-B Testing.md
---

# NES-1003 — Experimentation

> **"Data beats opinions. We validate feature improvements by designing structured, statistically significant product experiments."**

---

# Executive Summary

Making major product decisions based solely on gut feelings, subjective user surveys, or executive assumptions frequently leads to poor user retention and regression of business KPIs.

We standardize on an **Experimentation Framework** for all NeelStack products.

This standard establishes our hypothesis criteria, sample size calculations, metrics definitions, and statistical significance benchmarks.

---

# Purpose

This standard defines:

- Experimentation Core Principles
- Hypothesis Generation Guidelines
- Metric Tiers (OMTM, Guardrail, Secondary)
- Sample Size and Minimum Detectable Effect (MDE) Calculations
- Ethics and User Protection Boundaries

---

# Experimentation Core Principles

All product experiments must adhere to three core rules:

1. **Formulate Hypotheses Prior to Building**: Clearly document the expected user behavior change and the metrics that will measure it before writing code.
2. **Ensure Statistical Integrity**: Do not stop experiments early when metrics look favorable ("p-hacking"). Run experiments for the pre-calculated duration.
3. **Guardrail Metrics Protection**: Never optimize secondary metrics (e.g. click rate) in a way that degrades core system guardrail metrics (e.g. page load speed or error rates).

---

# Hypothesis Generation Standards

A valid experimentation hypothesis must be declared using the following structured template:

```text
We believe that: [Adding feature X / Modifying interface Y]
For: [Target user persona Z]
Will result in: [Specific outcome / User behavior change]
We will know this is true when: [Metric A increases by B% over baseline C]
Within: [Timeframe D]
```

---

# Metrics Framework Tiers

To prevent confusion and ensure alignment during analysis, classify metrics into three tiers:

- **One Metric That Matters (OMTM)**: The primary success metric that directly measures the hypothesis outcome (e.g. checkout conversion rate).
- **Secondary Metrics**: Metrics that explain the *why* behind OMTM shifts (e.g. add-to-cart clicks, time spent on checkout page).
- **Guardrail Metrics**: System-wide performance and security parameters that must not be degraded during the experiment (e.g. API latency, application crash rate, customer unsubscribe rate).

---

# Sample Size & MDE Calculations

Prior to launching any experiment, analysts must calculate the required sample size to prevent false positives:

- **Minimum Detectable Effect (MDE)**: Define the smallest relative change in the OMTM that is worth the cost of the change.
- **Statistical Parameters**: Standardize on:
  - **Statistical Power**: **80%** (20% chance of a false negative).
  - **Significance Level (Alpha)**: **5%** (5% chance of a false positive, p-value < 0.05).
- **Runtime Calculator**: Use the pre-calculated sample size to determine the exact duration (e.g. 14 days) required to collect sufficient user sessions.

---

# Anti-Patterns

❌ **P-Hacking (Peeking)**: Stopping an experiment early and declaring victory as soon as the p-value dips below 0.05. Metrics fluctuate early in runs. Tests must run for their full planned duration.

❌ **Ignoring Guardrail Degradation**: Celebrating a checkout flow feature that raises sales but causes API load times to double, violating system performance SLAs.

❌ **Excluding Baseline Comparisons**: Running feature experiments without an active control group (e.g. rolling out to 100% of users and comparing with the previous month), introducing seasonal skew variables.

---

# Production Checklist

- [ ] Experiment hypotheses are documented.
- [ ] OMTM, secondary, and guardrail metrics are defined.
- [ ] Sample size calculations are complete.
- [ ] Experiment duration is locked.
- [ ] LaunchDarkly targeting rules are verified.

---

# Success Criteria

The Experimentation program is successful when:
- Product changes are backed by statistically significant conversion gains.
- System performance is protected by automated guardrail metric monitors.
- User cohort evaluations show zero behavioral data anomalies.

---

# Document Status

**Document:** NES-1003 — Experimentation
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1004 — A-B Testing.md**
