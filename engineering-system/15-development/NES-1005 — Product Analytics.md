---
document_id: NES-1005
title: Product Analytics
subtitle: Enterprise Product Engagement Metrics & Conversion Funnel Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Product Analytics Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1004 A-B Testing
next_document: NES-1006 UX Research
---

# NES-1005 — Product Analytics

> **"If it is not tracked, it does not exist. We measure user engagement, calculate conversion rates, and audit adoption metrics dynamically."**

---

# Executive Summary

To optimize user retention and make informed product decisions, we must analyze how customers interact with our applications.

Relying on assumptions or raw database size metrics is insufficient to evaluate product health.

We mandate the tracking of user activity metrics using our **Product Analytics Framework** (integrated with **Segment / Amplitude / PostHog**).

This standard establishes our tracking requirements, core metrics (AARRR), conversion funnel tracking, and privacy compliance rules.

---

# Purpose

This standard defines:

- Product Analytics Tooling (Amplitude / PostHog)
- Core Metric Framework (AARRR Pirates Model)
- Conversion Funnel and Retention Calculations
- User Cohort Grouping
- Data Privacy Filters

---

# Core Product Telemetry Framework (AARRR)

We track the customer lifecycle using the **AARRR (Pirate Metrics)** framework:

| Lifecycle Phase | Metric Focus | Telemetry Event Example |
|---|---|---|
| **Acquisition** | Where do users come from? | `utm_source` captured on signup. |
| **Activation** | Do users have a good first experience? | `first_document_processed` event. |
| **Retention** | Do users come back? | `session_started` frequency. |
| **Referral** | Do users invite others? | `invitation_sent` event. |
| **Revenue** | How do we monetize? | `subscription_renewed` transaction value. |

---

# Conversion Funnel Calculations

Analyze user drop-off points to locate usability bottlenecks:

- **Funnel Definition**: Sequence of events leading to a target goal (e.g. `Landing Page` -> `Billing details entered` -> `Subscription active`).
- **Metric Target**: Track step-to-step conversion percentages. Drops exceeding **20%** between adjacent steps trigger UX review cards.
- **Query Standard**: Compile funnel charts dynamically using standard event properties (NES-705).

---

# Retention Cohort Mapping

Understand customer stickiness over time:

- **N-Day Retention**: Calculate the percentage of users who return to the app on exactly Day N after their signup.
- **Unbounded Retention**: Calculate the percentage of users who return on Day N or any day after.
- **Cohort Analysis**: Segment users by registration month (e.g., January Cohort) to track retention improvements across software version releases.

---

# Analytics Privacy Controls

To comply with global regulations (GDPR/HIPAA):

- **Data Masking**: Scrub input parameters containing names, phone numbers, or passwords prior to shipping to Amplitude.
- **ATT Opt-in**: On mobile devices, require App Tracking Transparency (ATT) permission before initializing third-party analytics trackers.

---

# Anti-Patterns

❌ **Tracking Raw UI Spacers**: Logging generic events like `hover_over_card_container`, which generates massive log volumes with no actionable product data.

❌ **Exposing Session IDs publicly**: Passing active session keys or authorization tokens inside analytics tracking URLs.

❌ **Omitting Retention Benchmarks**: Measuring success solely by new signup volume while ignoring high customer churn rates.

---

# Production Checklist

- [ ] Telemetry SDK (Amplitude/PostHog) is initialized.
- [ ] Core AARRR event hooks are mapped.
- [ ] Conversion funnels are declared.
- [ ] Geolocation routing maps to local data zones.
- [ ] Privacy filters remove customer PII.

---

# Success Criteria

The Product Analytics program is successful when:
- Product managers can generate conversion funnels without manual database exports.
- Retention curves confirm that customer stickiness is tracked by cohort.
- Data privacy audits show zero leaked PII in analytics datastores.

---

# Document Status

**Document:** NES-1005 — Product Analytics
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1006 — UX Research**
