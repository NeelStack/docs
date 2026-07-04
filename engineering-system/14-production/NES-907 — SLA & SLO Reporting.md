---
document_id: NES-907
title: SLA & SLO Reporting
subtitle: Enterprise SLA Uptime, SLO Error Budgets & Operations Reporting Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-906 Rollback Playbook
next_document: NES-908 Runbooks & Playbooks
---

# NES-907 — SLA & SLO Reporting

> **"Reliability is a promise. We track Service Level Agreements (SLAs), manage Service Level Objectives (SLOs), and report uptime metrics transparently."**

---

# Executive Summary

To maintain client trust and satisfy enterprise SLAs, we must monitor and report platform reliability metrics continuously.

If we define uptime subjectively or calculate SLAs manually using raw logs during billing cycles, reporting disputes will emerge.

We mandate the adoption of automated **SLA & SLO Reporting** across all NeelStack environments.

This standard establishes our uptime calculations, SLO targets, error budget management, and customer-facing status reporting pipelines.

---

# Purpose

This standard defines:

- Service Level Agreement (SLA) Targets
- Service Level Objective (SLO) Formulations
- Error Budget Management Policies
- Automated Uptime Calculations
- Public Status Page Reporting

---

# Service Level Agreement (SLA) Targets

Our SLAs are legal commitments to our enterprise clients.

- **Primary SLA Target**: Maintain a minimum **99.9%** availability monthly (e.g. max 43.8 minutes of unplanned downtime per month).
- **Billing Penalties**: Failure to meet SLAs triggers service credit penalties in client billing cycles.

---

# Service Level Objectives (SLOs)

Our internal SLOs are targets designed to keep us within SLA compliance limits.

- **Objective Formula**: Calculate SLOs using the ratio of successful requests over total requests:
  ```text
  SLO = (Successful Requests) / (Total Requests)
  ```
- **Example Targets**:
  - *Core API availability*: **99.95%** success rate.
  - *Write latency (p95)*: **< 300ms**.
  - *Read latency (p95)*: **< 100ms**.

---

# Error Budget Management

The Error Budget is the allowed downtime fraction before we violate our SLOs (e.g., a 99.9% SLO allows a 0.1% error rate).

- **Budget Consumed**: If error rates spike, the error budget is depleted.
- **Budget Exceeded Policy**:
  - **Action**: If a service consumes **100%** of its monthly error budget, all new feature releases are automatically suspended.
  - **Exceptions**: Only security patches (NES-607) and critical bug fixes can be promoted until the error budget is restored in the next cycle.

```text
  Error Budget Remaining: 100%  ──► releases active
  Error Budget Remaining: 50%   ──► warnings active
  Error Budget Remaining: 0%    ──► releases locked (only security hotfixes permitted)
```

---

# Automated Uptime Calculations

Uptime calculations must be automated using **Prometheus** metrics scraped from ingress load balancers.

- **Target Query**:
  ```text
  sum(rate(nginx_ingress_controller_requests{status!~"5.."}[5m])) / sum(rate(nginx_ingress_controller_requests[5m])) * 100
  ```
- **Exclusions**: Scheduled maintenance windows (notified at least 48 hours in advance) are excluded from monthly SLA calculations.

---

# Public Status Page

Uptime status must be communicated transparently.

- **Automated Sync**: Connect monitoring systems directly to our public status page (e.g. status.neelstack.com).
- **Incident Logs**: When an incident occurs, the Incident Commander (NES-518) must update the status page within 15 minutes of outage confirmation.

---

# Anti-Patterns

❌ **Manual Log Sifting**: Calculating monthly uptime by grepping server log files at the end of the month, which is prone to errors.

❌ **Excluding Third-Party Outages**: Omitting outages caused by third-party database dependencies from SLA calculations. If our platform is down, the client experiences it as downtime, regardless of the cause.

❌ **Silent Status Pages**: Keeping status pages "Green" during active customer outages to avoid reporting incidents.

---

# Production Checklist

- [ ] Internal SLOs are configured in Prometheus rules.
- [ ] Error budget alerts are active.
- [ ] Public Status Page is integrated with monitoring systems.
- [ ] Monthly SLA reports are generated automatically.
- [ ] SLA exclusion windows are registered in the tracking calendar.

---

# Success Criteria

The SLA/SLO program is successful when:
- Internal SLO alert targets trigger before legal SLA limits are breached.
- Operations teams manage error budgets to guide release planning.
- Uptime calculations are automated, repeatable, and audit-ready.

---

# Document Status

**Document:** NES-907 — SLA & SLO Reporting
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-908 — Runbooks & Playbooks**
