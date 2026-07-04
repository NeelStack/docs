---
document_id: NES-810
title: Bug Tracking
subtitle: Enterprise Defect Lifecycle, Jira Workflows & Priority Matrix Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Quality Assurance Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-809 UAT
next_document: NES-811 Test Automation
---

# NES-810 — Bug Tracking

> **"Bugs must be logged, triaged, and resolved systematically. We enforce structured Jira workflows and strict priority-severity matrices."**

---

# Executive Summary

Software bugs vary in impact, from simple typos to critical database crashes.

If bugs are logged in unstructured notes, discussed only in chat channels, or prioritized subjectively, resolution is delayed, leading to open backlogs and release blocks.

We mandate the centralization of all software defects under a unified **Bug Tracking Workflow** inside our task management platform (**Jira**).

This standard establishes our defect severity classifications, priority definitions, triage workflows, and hotfix promotion rules.

---

# Purpose

This standard defines:

- Defect Severity vs. Priority Matrix
- Centralized Jira Bug Tracking Workflow
- Mandatory Bug Report Templates
- Triage and Allocation SLA Rules
- Hotfix Promotion Protocols

---

# Severity vs. Priority Matrix

We separate **Severity** (technical impact on the system) from **Priority** (business urgency for resolution):

### 1. Severity Levels (Technical Impact)
- **S1 (Blocker)**: System crash, data corruption, security leak, major API down.
- **S2 (Critical)**: Feature broken with no workaround.
- **S3 (Major)**: Feature broken but workarounds exist.
- **S4 (Trivial)**: Cosmetic UI issue, typo, minor design alignment error.

### 2. Priority Levels (Business Urgency)
- **P0 (Immediate)**: Fix immediately. SRE hotfix triggered.
- **P1 (High)**: Resolve in the active sprint cycle.
- **P2 (Medium)**: Schedule in the upcoming product roadmap backlog.
- **P3 (Low)**: Remediate on best-effort basis.

---

# Centralized Bug Tracking Workflow

Bugs follow a strict, audited lifecycle state progression in Jira:

```text
  [ New / Logged ] ──► [ Triaged ] ──► [ In Progress ]
                             │               │
                             ▼               ▼
                        [ Rejected ]   [ Code Review ]
                             │               │
                             ▼               ▼
                        [ Archive ]      [ Testing ] ──► [ Resolved ]
```

- **Reopen Rule**: If a QA engineer validates a bug patch in staging and finds the issue unresolved, the ticket state must return to "In Progress" with explanatory logs.

---

# Bug Report Template

To ensure developers have all details needed to fix defects, all Jira bug tickets must utilize the following markdown schema:

```text
## Description
Brief summary of the issue.

## Environment
- OS: iOS 17.2, macOS Sonoma
- Browser: Safari 17.2
- Environment: Staging-VPC-2

## Steps to Reproduce
1. Log in with user credentials.
2. Navigate to /invoices/compile.
3. Click "Submit".

## Expected Behavior
Invoice compiles and shows a success dialog.

## Actual Behavior
Screen freezes, and browser console shows 'TypeError: undefined is not an object'.

## Attachments
[Link to screenshots / video recordings / console log outputs]
```

---

# Triage & SLA Timeframes

Data domain owners must review and triage incoming bugs daily.

- **SLA for Triage**: S1/S2 bugs must be triaged within **2 hours** of logging.
- **Resolution SLA**: P0 bugs must be patched, verified, and deployed within **24 hours**.

---

# Anti-Patterns

❌ **Direct Developer Messaging**: Alerting developers to bugs directly in chat channels (e.g. Slack) instead of logging a ticket in Jira.

❌ **Closing Bugs without Verification**: Developers closing bug tickets as "Resolved" before QA has tested the patch in staging.

❌ **Over-escalation**: Marking minor cosmetic bugs as S1/P0 to speed up resolution, leading to alert fatigue.

---

# Production Checklist

- [ ] Jira bug tracking workflow is configured.
- [ ] Bug report template is active on Jira projects.
- [ ] Triage alerts are routed to Slack channels.
- [ ] Priority definitions are documented.
- [ ] Verification steps are recorded on resolved tickets.

---

# Success Criteria

The Bug Tracking program is successful when:
- Average Time to Resolve (MTTR) for S1/P0 bugs remains under 24 hours.
- Defect reports contain reproducible steps, reducing diagnostic delays.
- Resolved bugs are verified in staging before closing.

---

# Document Status

**Document:** NES-810 — Bug Tracking
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-811 — Test Automation**
