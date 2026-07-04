---
document_id: NES-518
title: Incident Response
subtitle: Enterprise Incident Management, On-Call & Post-Mortem Standard
version: 1.0.0
status: Draft
classification: Internal
owner: SRE & Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-517 Logging
next_document: NES-519 Disaster Recovery
---

# NES-518 — Incident Response

> **"Incidents are inevitable. Resolving them rapidly requires clear roles, dry-run runbooks, and blame-free post-mortems."**

---

# Executive Summary

Outages and degradation of service affect our customers and cause financial loss.

During an active outage, developers must not argue over responsibility or troubleshoot without structure.

This standard establishes the incident severity classifications, on-call paging hierarchies (PagerDuty), incident commander roles, and the mandatory blame-free post-mortem process.

---

# Purpose

This standard defines:

- Incident Severity Levels (SEV-1 to SEV-3)
- On-Call Paging and Escalation Rules
- Incident Commander (IC) Responsibilities
- Diagnostic Runbook Standards
- Post-Mortem and Root Cause Analysis (RCA)

---

# Incident Severity Classifications

We classify operational issues into three severity levels:

| Level | Definition | Impact | SLA Target |
|---|---|---|---|
| **SEV-1 (Critical)** | Core service down globally (e.g. database down). | Hundreds of users affected, billing blocked. | Acknowledge in <5m, resolve <2h. |
| **SEV-2 (Major)** | Major feature degraded (e.g. OCR API returning 500s). | Workarounds exist, single tenant affected. | Acknowledge <15m, resolve <8h. |
| **SEV-3 (Minor)** | UI alignment issue, minor bug in non-critical flow. | Minimal business impact. | Resolve next release cycle. |

---

# On-Call & PagerDuty Escalations

We use **PagerDuty** to handle alert routing and escalation schedules.

- **Escalation Rules**: If an alert is not acknowledged by the primary on-call SRE within **10 minutes**, PagerDuty escalates it to the secondary lead. If still unacknowledged after 20 minutes, it alerts the Engineering Manager.
- **Alert Quality**: Only trigger paging alerts for actionable SEV-1 and SEV-2 failures. Non-actionable alerts must be logged to Slack channels as warnings to prevent alert fatigue.

---

# Incident Commander (IC) Role

During a SEV-1 incident, one person must assume the role of **Incident Commander (IC)**.

- **Primary Duty**: The IC does not debug code or inspect logs. They coordinate communication, assign diagnostic tasks to engineers, and post status updates (e.g. every 30 minutes) on the customer status page.
- **Authority**: The IC has full authority to roll back releases, spin down resources, or close network connections to protect customer data.

---

# Diagnostic Runbook Standards

Every production microservice must maintain a `RUNBOOK.md` in its repository.

- **Standard**: Runbooks must contain step-by-step instructions for troubleshooting common failure modes (e.g. "Database CPU spike", "Kafka queue backing up").
- **No Ambiguity**: Instructions must be written with explicit commands (e.g. run this kubectl command) to support rapid resolution by developers unfamiliar with the service.

---

# Blame-Free Post-Mortems

Every SEV-1 and SEV-2 incident requires a **Post-Mortem** within **48 hours** of resolution.

- **Blame-Free Culture**: Focus on identifying system gaps, not human errors. We ask "Why did the system allow this to happen?" rather than "Who did it?".
- **Action Items**: Post-mortems are successful only if they yield actionable tickets (prefixed with `INCIDENT-FIX`) to prevent the same failure mode from occurring again.

---

# Anti-Patterns

❌ **Silent Outages**: Keeping customers in the dark during an outage without updating status pages, which erodes trust.

❌ **By-passing Post-Mortems**: Declaring an incident resolved and moving on without documenting lessons or scheduling corrective tasks.

❌ **Alerting on Everything**: Routing disk utilization warnings (e.g. 70% full) as critical SMS pages in the middle of the night.

---

# Production Checklist

- [ ] PagerDuty escalation policies are configured for every service.
- [ ] Central Status Page integration is active.
- [ ] Every repository contains a validated `RUNBOOK.md` file.
- [ ] Post-mortem meeting template is shared and versioned.
- [ ] Team contact matrix is updated.

---

# Success Criteria

The Incident Response system is successful when:
- Average Time to Acknowledge (MTTA) for critical issues is under 5 minutes.
- Average Time to Resolve (MTTR) decreases year-over-year.
- The post-mortem corrective action items are completed within two sprint cycles of the incident.

---

# Document Status

**Document:** NES-518 — Incident Response
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-519 — Disaster Recovery**
