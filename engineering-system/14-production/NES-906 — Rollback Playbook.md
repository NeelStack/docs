---
document_id: NES-906
title: Rollback Playbook
subtitle: Enterprise Emergency Rollback & Database Recovery Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-905 Canary Releases
next_document: NES-907 SLA & SLO Reporting
---

# NES-906 — Rollback Playbook

> **"A release is not complete without a verified rollback path. We document, automate, and execute rollback plans for all software systems."**

---

# Executive Summary

When a software release introduces critical production errors, security vulnerabilities, or database lockups, operations teams must restore service quickly.

Attempting to diagnose code, write patches, and push hotfixes while the platform is down increases downtime.

The fastest path to recovery is a **Rollback**.

This standard establishes our emergency rollback trigger conditions, command-level instructions, database recovery checklists, and post-rollback audits.

---

# Purpose

This standard defines:

- Rollback Trigger Parameters
- Command-level Rollback Execution Steps
- Database Schema Rollback Safety Checkpoints
- Automated Rollback Pipelines Configuration
- Post-Rollback Audits Requirements

---

# Rollback Trigger Parameters

An emergency rollback must be initiated immediately if any of the following conditions occur post-deployment:

- **Availability Drop**: Uptime metrics fall below **99.9%** (measured over 5 minutes).
- **Critical Path Broken**: Payment gateways, customer logins, or file uploads return 5xx errors.
- **Resource Starvation**: Compute pods experience CPU/Memory saturation or crash loops.
- **Database Lockup**: Database CPU usage remains at 100% due to un-indexed query loads.

---

# Rollback Execution Steps

Follow these steps to rollback a failed release:

```text
  Incident Detected
         │
         ▼
 1. Shift Traffic to Old Version
 ├── Update Istio VirtualService weights to 0% on Canary
 └── Or update ALB target group mapping to Blue environment
         │
         ▼
 2. Verify System Health restores
         │
         ▼
 3. Terminate failed Green containers
         │
         ▼
 4. Log Post-Rollback incident review
```

---

# Database Rollback Safety

Modifying database schemas during a rollback carries high risk:

- **Never Roll Back Database Migrations Automatically**: If a new release has written records to a new schema, rolling back the database tables can cause data loss.
- **Rule**: Retain the new schema structures. Keep the database configuration in the "Expanded" state (NES-904) and route the rolled-back application build to read from the backward-compatible schemas.
- **Data Reconciliation**: SREs must write cleanup scripts to extract, transform, and merge any records written to new columns during the compromised deployment window back into legacy schemas.

---

# Automated Rollback Pipelines

Configure automated rollbacks inside CI/CD configurations:

- **ArgoCD rollback**: Use the `argocd app rollback` CLI command to revert Kubernetes resources to the previous git tag automatically if health checks fail:
  ```bash
  argocd app rollback portal-api --revision 83a74e98
  ```

---

# Post-Rollback Audits

Within **24 hours** of executing a manual or automated rollback:

- **Post-Mortem**: SRE and developer teams must host a blame-free post-mortem (NES-909) to identify the root cause of the deployment failure.
- **Remediation**: Corrective tasks must be logged in Jira (prefixed with `DEPLOY-FIX`) before the team can attempt another release run for the service.

---

# Anti-Patterns

❌ **Rolling Forward during Outages**: Attempting to debug and push new code patches to production during an active outage instead of executing a rollback.

❌ **Auto-dropping Database Tables**: Writing migration scripts that run drop commands automatically during rollbacks, causing permanent customer data loss.

❌ **Excluding Rollback dry-runs**: Failing to test rollback procedures in staging, leading to failure discovery during live outages.

---

# Production Checklist

- [ ] Automated rollback triggers are verified.
- [ ] ArgoCD rollback configs are active.
- [ ] Database migrations follow backward-compatibility rules.
- [ ] Rollback execution commands are documented in service runbooks.
- [ ] Monitoring system flags and alerts are active.

---

# Success Criteria

The Rollback program is successful when:
- Average Time to Revert (MTTR) a compromised release is under 2 minutes.
- Rollbacks are executed without causing database integrity failures or data loss.
- Post-rollback logs document the root cause and remediation steps.

---

# Document Status

**Document:** NES-906 — Rollback Playbook
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-907 — SLA & SLO Reporting**
