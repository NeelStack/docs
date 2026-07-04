---
document_id: NES-1001
title: Roadmaps
subtitle: Enterprise Product Roadmaps, Prioritization & Outcome-Based Planning Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Product Management Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1000 Product Discovery
next_document: NES-1002 Feature Lifecycle
---

# NES-1001 — Roadmaps

> **"Roadmaps map outcomes, not dates. We plan releases based on customer value, strategic objectives, and engineering capacity limits."**

---

# Executive Summary

Traditional feature-based product roadmaps (listing specific features tied to hard calendar dates months in advance) fail because they encourage developers to prioritize shipping dates over business value, causing quality issues.

We mandate **Outcome-Based Roadmaps** across all NeelStack products.

This standard establishes our roadmap structure, prioritization frameworks (RICE), capacity planning rules, and release alignment targets.

---

# Purpose

This standard defines:

- Outcome-Based Roadmaps Structure (Now, Next, Later)
- Prioritization Framework (RICE)
- Engineering Capacity Allocation
- Cross-Functional Team Alignment
- Roadmap Update Cycles

---

# Outcome-Based Roadmaps (Now, Next, Later)

We prohibit the use of static Gantt charts showing exact delivery dates. We organize roadmaps into three priority time horizons:

- **Now**: Active sprint commitments (current quarter). High certainty, defined metrics, and active development focus.
- **Next**: Planned candidates (next quarter). High value, under active discovery, and currently being threat-modeled.
- **Later**: Strategic opportunities (future quarters). Backlog items aligned with the long-term vision (NES-001).

---

# Prioritization Framework (RICE)

Evaluate backlog items objectively using the **RICE** score model:

```text
RICE Score = ( Reach × Impact × Confidence ) / Effort
```

- **Reach**: Number of active users affected in a defined period (e.g. per quarter).
- **Impact**: Business value scale (3 = Massive, 2 = High, 1 = Medium, 0.5 = Low).
- **Confidence**: Data backing our assumptions (100% = High data, 80% = Qualitative research, 50% = Low data).
- **Effort**: Person-months of engineering time required (determined by tech leads).

---

# Engineering Capacity Allocation

To maintain platform stability, prevent technical debt accumulation, and avoid developer burnout, assign sprint capacity according to the following allocations:

```text
 ┌────────────────────────────────────────────────────────┐
 │  New Features / Product Discovery (Now Category) - 60%  │
 ├────────────────────────────────────────────────────────┤
 │  Technical Debt / Architecture / Scale (NES-1101) - 20% │
 ├────────────────────────────────────────────────────────┤
 │  Bug Fixes / Maintenance / Security Patches - 20%       │
 └────────────────────────────────────────────────────────┘
```

---

# Roadmap Review & Communication

Roadmaps are living documents:

- **Monthly Review**: Product managers and tech leads must review active roadmap goals monthly to adjust weights based on analytics.
- **Stakeholder Transparency**: Publish updated roadmaps to the central portal to align marketing, support, and sales teams on upcoming feature rollouts.

---

# Anti-Patterns

❌ **Hard-Dated Feature Promises**: Publicly promising enterprise clients a complex feature on an exact calendar date without completing technical discovery.

❌ **Excluding Tech Debt from Planning**: Allocating 100% of engineering capacity to new features, causing system performance drops and code degradation over time.

❌ **Subjective Prioritization**: Adding items to the roadmap based solely on the opinions of the loudest stakeholders instead of using objective RICE scoring.

---

# Production Checklist

- [ ] Product roadmaps utilize the "Now, Next, Later" format.
- [ ] RICE prioritization scores are calculated for backlog candidates.
- [ ] Engineering capacity limits are respected in sprint planning.
- [ ] Monthly roadmap alignment sessions are scheduled.
- [ ] Roadmap targets map to active product KPIs.

---

# Success Criteria

The Product Roadmap system is successful when:
- 100% of planned roadmap items are backed by objective business value metrics.
- Tech debt remediation tasks are allocated consistent sprint resources.
- Teams adjust release sequences dynamically without disrupting active client systems.

---

# Document Status

**Document:** NES-1001 — Roadmaps
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1002 — Feature Lifecycle**
