---
document_id: NES-1104
title: Capability Maturity
subtitle: Enterprise Engineering Capability Maturity Model & Assessment Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Governance Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1103 Architecture Review Board
next_document: NES-1105 Internal Certifications
---

# NES-1104 — Capability Maturity

> **"Maturity is a measure of operational consistency. We evaluate our engineering processes, identify capability levels, and target continuous improvement."**

---

# Executive Summary

Without an objective framework to assess engineering practices, teams can operate with inconsistent quality, leading to performance variations and slow delivery speeds.

We mandate the adoption of the **NeelStack Engineering Capability Maturity Model (NECMM)**.

This standard establishes our maturity level definitions, assessment criteria across key domains, and team self-evaluation protocols.

---

# Purpose

This standard defines:

- NECMM Maturity Levels (1 to 5)
- Assessment Domains (Delivery, Quality, Operations)
- Team Self-Assessment Protocols
- Target Maturity States
- Continual Improvement Guidelines

---

# NECMM Maturity Levels

We classify engineering capability maturity into five levels:

| Level | Classification | Description |
|---|---|---|
| **Level 1** | **Initial** | Processes are ad-hoc, inconsistent, and depend on individual heroics. |
| **Level 2** | **Repeatable** | Basic project management and version control are established. |
| **Level 3** | **Defined** | Processes are documented, standardized, and integrated into workflows. |
| **Level 4** | **Managed** | Processes are measured quantitatively using DORA and quality metrics. |
| **Level 5** | **Optimizing** | Focus is on continuous process improvement and automated optimization. |

---

# Assessment Domains

Evaluate team maturity across four primary operational domains:

- **Software Delivery**: Version control, code reviews, and deployment automation frequency.
- **Quality Assurance**: Unit test coverage, automated E2E checks, and bug resolution rates.
- **Operations & Security**: Real-time logging, security scanning, vulnerability SLAs compliance, and incident response.
- **Product & Governance**: Product discovery, roadmap metrics mapping, and architecture review compliance.

---

# Assessment Protocols

Ensure objective capability reviews:

- **Self-Assessment**: Teams must conduct a capability self-assessment every **6 months** using the standardized NECMM rubric.
- **Moderation**: SRE leads and architects moderate self-assessments to verify consistency across product divisions.
- **Improvement Plan**: Teams scoring below Level 3 in any domain must document an **Actionable Improvement Plan** to address capability gaps in upcoming sprints.

---

# Continual Improvement Sprints

Maturity level targets are updated annually:

- **Target State**: All teams are expected to maintain at least a **Level 3 (Defined)** capability rating across core domains.
- **Optimizing**: Teams at Level 4 are encouraged to automate testing and deployment feedback loops further to target Level 5 optimization.

---

# Anti-Patterns

❌ **Static Maturity Scores**: Treating maturity reviews as point-in-time compliance checks without taking action to improve processes.

❌ **Excluding Core Domains**: Assessing only delivery speed while ignoring quality assurance or security compliance gaps.

❌ **Ranking Teams Punitively**: Using maturity assessments to compare teams punitively, leading to biased self-evaluations.

---

# Production Checklist

- [ ] NECMM assessment rubric is published.
- [ ] Team assessment calendars are scheduled.
- [ ] Improvement plan templates are prepared.
- [ ] Moderation workflows are active.
- [ ] Maturity metrics dashboards are configured.

---

# Success Criteria

The Capability Maturity program is successful when:
- 100% of engineering teams achieve and maintain at least a Level 3 rating.
- Assessment reviews identify and address operational capability bottlenecks.
- Platform development speeds and stability metrics improve over time.

---

# Document Status

**Document:** NES-1104 — Capability Maturity
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1105 — Internal Certifications**
