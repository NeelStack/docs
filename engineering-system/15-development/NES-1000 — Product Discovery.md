---
document_id: NES-1000
title: Product Discovery
subtitle: Enterprise Product Discovery, Opportunity Assessment & Validation Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Product Management Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-911 Reference Architecture
next_document: NES-1001 Roadmaps
---

# NES-1000 — Product Discovery

> **"Build the right thing before building it right. We validate user needs, assess business feasibility, and define product value before writing system code."**

---

# Executive Summary

Developing complex software features based on assumptions or untested user requirements leads to unused product capabilities, wasted engineering resources, and bloated codebases.

We mandate a structured **Product Discovery** process for all new products, major features, and integrations across the NeelStack ecosystem.

This standard establishes our opportunity assessment framework, user persona mapping protocols, risk mitigation strategies, and validation gates.

---

# Purpose

This standard defines:

- Product Discovery Principles
- Opportunity Assessment (Marty Cagan's 10 Questions)
- The Four Product Risks (Value, Usability, Feasibility, Viability)
- User Persona and Journey Mapping
- Discovery Phase Gates and Approvals

---

# Product Discovery Principles

Our product discovery is guided by three core rules:

1. **Focus on Outcomes, Not Outputs**: Success is measured by business value and user adoption, not by the volume of code pushed to repository branches.
2. **Shared Understanding**: Product managers, lead developers, and UX designers collaborate during the discovery phase to align on constraints.
3. **Continuous Discovery**: Regularly interview users, inspect usage analytics, and refine requirements to adapt to market feedback.

---

# Marty Cagan's Opportunity Assessment

Before scheduling feature work into sprint queues, product managers must document an Opportunity Assessment answering:

- Exactly what business objective does this feature address?
- What customer problem are we solving?
- Who is the target user or customer persona?
- How will we measure success (what KPIs will move)?
- Why are we uniquely positioned to build this solution?

---

# The Four Product Risks

Discovery validation must address four core product risks:

| Risk Category | Definition | Verification Method |
|---|---|---|
| **Value Risk** | Will the customer buy this or choose to use it? | User interviews, interactive prototypes. |
| **Usability Risk** | Can the user figure out how to navigate it? | UX research sessions, cognitive walkthroughs. |
| **Feasibility Risk** | Can our engineers build this with available tech? | Spike tasks, architectural reviews. |
| **Viability Risk** | Does this solution work for our business? | Financial reviews, legal/regulatory checks (GDPR). |

---

# User Persona & Journey Mapping

All feature designs must map to verified **User Personas**:

- **Persona Profile**: Document the user's role, objectives, frustrations, and environment context (e.g. "School Registrar in EduOS", "Clinician in DhruvaOS").
- **Journey Map**: Diagram the user's workflow path from discovery to feature completion, identifying friction points and system boundaries.

---

# Discovery Gating & Approvals

Promoting a product concept to the active engineering backlog requires:

- [ ] Completed Opportunity Assessment registered in the product database.
- [ ] Prototypes validated by UX research user testing sessions.
- [ ] Technical feasibility signed off by the engineering lead.
- [ ] Compliance verification (GDPR/HIPAA) completed.

---

# Anti-Patterns

❌ **Building without Discovery**: Launching development cycles based solely on executive directives without validating customer demand, leading to low adoption.

❌ **Isolated Feature Spec Sheets**: Writing detailed 50-page requirement documents in isolation and handing them off to developers, bypassing collaborative design.

❌ **Ignoring Feasibility Constraints**: Designing complex interfaces that require unavailable technologies or database architectures, forcing late-stage rebuilds.

---

# Production Checklist

- [ ] Opportunity assessment documents are version-controlled.
- [ ] User personas map to all core product areas.
- [ ] Feasibility spike tasks are scheduled in JIRA.
- [ ] Value validation metrics are active.
- [ ] Discovery gates are integrated with project workflows.

---

# Success Criteria

The Product Discovery process is successful when:
- Features scheduled for development demonstrate high user adoption rates post-release.
- Engineering cycles are not wasted on cancelled or heavily modified designs.
- Feasibility risks are identified and resolved before core development starts.

---

# Document Status

**Document:** NES-1000 — Product Discovery
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1001 — Roadmaps**
