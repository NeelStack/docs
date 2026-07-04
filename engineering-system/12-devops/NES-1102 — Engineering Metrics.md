---
document_id: NES-1102
title: Engineering Metrics
subtitle: Enterprise DORA Metrics, Code Quality & Productivity Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1101 Technical Debt
next_document: NES-1103 Architecture Review Board
---

# NES-1102 — Engineering Metrics

> **"If it is not measured, it is not managed. We track engineering performance, DORA metrics, and codebase health using automated dashboards."**

---

# Executive Summary

Evaluating engineering performance using subjective metrics or raw commit counts leads to misaligned teams, poor code quality, and slow release cycles.

We mandate the tracking of standardized **Engineering Metrics** across all NeelStack divisions.

This standard establishes our core delivery metrics (**DORA**), code complexity parameters, and developer productivity boundaries.

---

# Purpose

This standard defines:

- DevOps Research and Assessment (DORA) Metrics
- Code Quality and Complexity Metrics
- Developer Experience (DX) and Productivity Metrics
- Automated Metric Dashboard Tooling
- Metrics Usage and Privacy Safeguards

---

# DORA Delivery Metrics

We evaluate delivery speed and operational stability using the four core **DORA** metrics:

| DORA Metric | Definition | Target Threshold (Elite) |
|---|---|---|
| **Deployment Frequency** | How often code is successfully deployed to production. | **Multiple times per day** |
| **Lead Time for Changes** | Time taken from commit check-in to production deploy. | **< 1 Day** |
| **Change Failure Rate** | Ratio of deployments that cause production failures. | **< 5%** |
| **Failed Service Restore (MTTR)** | Time taken to restore service after a deployment failure. | **< 1 Hour** |

---

# Codebase Quality & Complexity Metrics

Automate codebase health tracking inside integration pipelines:

- **Cognitive Complexity**: Track class and method complexity metrics (using SonarQube). Block merges if functions exceed complexity thresholds.
- **Code Coverage**: Enforce the **80% line coverage** requirement on all pull requests (NES-802).
- **Duplicate Code**: Prohibit duplication levels exceeding **5%** in a single codebase.

---

# Developer Experience (DX) & Productivity

Measure pipeline efficiency and developer friction:

- **Build Duration**: Track CI pipeline execution times. Build runs must complete in under **5 minutes** (NES-811).
- **Pull Request Lifecycle**: Track the time elapsed from PR creation to merge (target: < 24 hours). Identify bottlenecks in peer code reviews.

---

# Metrics Usage & Privacy Boundaries

To maintain trust and psychological safety:

- **No Individual Rankings**: We prohibit the use of metrics to rank individual developers or guide performance reviews. Metrics are used to evaluate team processes and system efficiency.
- **Automated Dashboards**: Consolidate metrics into team-level dashboards (using tools like Apache DevLake or custom Grafana queries), tracking trends over time.

---

# Anti-Patterns

❌ **Ranking by Commit Count**: Evaluating developer performance based on commit volume or lines of code written. This encourages bloated codebases and artificial commits.

❌ **Excluding Staging Outages from MTTR**: Measuring MTTR only for production failures while ignoring staging stability issues, masking deployment bottlenecks.

❌ **Leaving Metrics Undocumented**: Collecting performance metrics without documenting baseline targets or taking action to improve pipeline bottlenecks.

---

# Production Checklist

- [ ] DORA metrics tracking is automated.
- [ ] Code complexity analysis (SonarQube) is active.
- [ ] CI pipeline execution times are monitored.
- [ ] Team-level metrics dashboards are active.
- [ ] Metrics usage policies are published.

---

# Success Criteria

The Engineering Metrics program is successful when:
- DORA metrics indicate elite-level deployment speeds and stability.
- Automated code reviews flag and block complex configurations before merge.
- Pipeline optimizations keep build execution times under 5 minutes.

---

# Document Status

**Document:** NES-1102 — Engineering Metrics
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1103 — Architecture Review Board**
