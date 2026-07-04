---
document_id: NES-1101
title: Technical Debt
subtitle: Enterprise Technical Debt Management, Budgeting & Resolution Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Architecture Review Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-1100 Enterprise Governance
next_document: NES-1102 Engineering Metrics
---

# NES-1101 — Technical Debt

> **"Technical debt is a financial metaphor. We track technical debt systematically, allocate refactoring budgets, and prevent codebase decay."**

---

# Executive Summary

To ship features quickly, software teams occasionally select tactical, short-term implementations that deviate from engineering standards.

This creates "Technical Debt."

If tech debt is not logged, managed, and resolved systematically, it accumulates over time, leading to slow release cycles, regression bugs, and eventual platform stagnation.

We mandate a formal **Technical Debt Management** framework.

This standard establishes our debt classification rules, technical budgeting criteria, and remediation workflows.

---

# Purpose

This standard defines:

- Technical Debt Classifications
- Tech Debt Registry and Logging Rules
- The 20% Sprint Capacity Allocation Budget
- Technical Debt Audit Sweeps
- Code Refactoring Checkpoints

---

# Technical Debt Classifications

We categorize technical debt into three profiles to guide priority scheduling:

- **Deliberate Debt**: Tactical shortcuts chosen consciously to hit critical business deadlines (e.g. implementing basic auth quickly with plans to upgrade to OIDC).
- **Accidental Debt**: Debt generated as technologies evolve or business requirements expand (e.g. legacy database queries running slowly under new traffic volumes).
- **Prudent Debt**: Minor code quality gaps (missing documentation, low coverage) that do not block systems but increase maintenance times.

---

# Tech Debt Registry & JIRA Logging

Tech debt must be documented, not hidden:

- **Jira Tracking**: All identified technical debt must be logged as tickets in JIRA, prefixed with `TECH-DEBT` (e.g. `TECH-DEBT: Migrate portal legacy raw SQL queries to ORM`).
- **Estimation**: Tech debt tickets must estimate the "Interest Rate" (how much extra time developers waste on tasks because this code remains unfixed) and the "Principal Cost" (estimated weeks of work needed to resolve it).

---

# The 20% Technical Budget Enforcements

To prevent codebase decay, teams must allocate resources systematically:

- **Resource Rule**: All development sprints must allocate **20% of engineering capacity** to resolving active `TECH-DEBT` tickets (NES-1001).
- **Product Override**: Product managers cannot override this 20% allocation unless the engineering lead approves an emergency exception.

---

# Bi-annual Technical Debt Sweeps

Maintain codebase hygiene:

- Tech leads must coordinate a **Technical Debt Sweep every 6 months**.
- During the sweep, compile code complexity metrics (SonarQube logs), review flaky tests, audit deprecated third-party packages, and prioritize the top 3 items in the `TECH-DEBT` registry.

---

# Anti-Patterns

❌ **Hiding Debt**: Permitting developers to implement temporary hotfixes or shortcuts without logging matching `TECH-DEBT` tickets, leaving the debt untracked.

❌ **Excluding Tech Debt from Sprints**: Allocating 100% of sprint capacity to new commercial features, leading to system performance degradation and developer burnout.

❌ **Refactoring without Tests**: Attempting to resolve technical debt by refactoring core codeblocks without verifying unit or integration test coverage first.

---

# Production Checklist

- [ ] `TECH-DEBT` ticket workflows are configured in Jira.
- [ ] Sprint templates enforce the 20% tech budget rule.
- [ ] Code complexity metrics are tracked via SonarQube.
- [ ] Technical debt sweeps are scheduled bi-annually.
- [ ] Refactoring tasks require peer-review sign-offs.

---

# Success Criteria

The Technical Debt program is successful when:
- Codebases maintain low complexity metrics (A-grade rating on SonarQube).
- Sprint planners systematically allocate resources to refactoring tasks.
- System performance and deployment speeds remain stable as features scale.

---

# Document Status

**Document:** NES-1101 — Technical Debt
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1102 — Engineering Metrics**
