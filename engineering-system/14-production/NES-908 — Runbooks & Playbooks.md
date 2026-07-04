---
document_id: NES-908
title: Runbooks & Playbooks
subtitle: Enterprise Runbook Standards, Incident Diagnostics & Actionable Command Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-907 SLA & SLO Reporting
next_document: NES-909 Incident Post-Mortems
---

# NES-908 — Runbooks & Playbooks

> **"Unplanned outages require planned actions. We write structured, executable runbooks for all microservices to guide rapid incident diagnostics."**

---

# Executive Summary

During a critical production outage (SEV-1), every minute of downtime costs revenue and erodes client trust.

Expecting on-call engineers to diagnose failures, locate databases, and execute commands under stress without documented guidelines leads to errors and increases resolve times (MTTR).

We mandate that all microservices, databases, and platform integrations maintain an active, verified **Runbook**.

This standard establishes our runbook structures, repository storage rules, and command-level documentation guidelines.

---

# Purpose

This standard defines:

- Standardized Runbook Layouts
- Diagnostic Command Formatting
- Repository Storage Conventions
- Maintenance and Verification Schedulers
- Runbook Accessibility Rules

---

# Runbook Directory & Storage

Runbooks must reside inside the same repository as the service code:

- **Location**: Store runbooks in the repository under `docs/ops/RUNBOOK.md`.
- **Reason**: Storing runbooks alongside code ensures developers can update documentation dynamically in the same pull requests that alter service structures.

---

# Standard Runbook Layout

All runbooks must conform to a standardized markdown template to ensure SREs can find diagnostic steps quickly:

```markdown
# [Service Name] Runbook

## Overview
Brief description of the service and its dependencies.

## Key Contacts
- Tech Lead: [@lead-username]
- Slack Channel: [#ops-channel]
- PagerDuty Service Link: [URL]

## Alerts Diagnostic Guide
Index of Prometheus alerts and step-by-step diagnostic actions.

### Alert: DatabaseCPUSpike
- **Symptom**: CPU utilization exceeds 90% on RDS Postgres.
- **Verification Command**:
  ```bash
  aws rds describe-db-instances --db-instance-identifier portal-prod-rds --query "DBInstances[0].CPUUtilization"
  ```
- **Remediation Steps**:
  1. Identify slow queries: Run SQL query script.
  2. Kill locking processes using PG Admin CLI script.

## System Restart & Scaling
- Scale commands: `kubectl scale deployment/portal-api --replicas=5 -n portal-prod`
```

---

# Diagnostic Command Formatting

Runbook instructions must be explicit and copy-pasteable:

- **Use Complete Commands**: Avoid placeholder commands (e.g. `run pg-kill-script`). Write the complete terminal command using parameters.
- **Explicit Parameter Flags**: Document parameter flags (e.g. specify the target namespace `-n portal-prod`) to prevent commands from running against the wrong environment.

---

# Runbook Verification & Game Days

Documentation decays over time if not verified.

- **Bi-annual Verification**: During scheduled **Disaster Recovery Game Days (NES-910)**, on-call engineers must execute the steps in service runbooks to confirm instructions are accurate and complete.
- **Pruning**: Remove outdated runbooks of decommissioned services.

---

# Anti-Patterns

❌ **Out-of-Date Wikis**: Storing runbooks on stale intranet wiki pages or Google Docs. Wikis are rarely updated when features change.

❌ **Exposing Secret Tokens**: Hardcoding passwords, database tokens, or AWS credentials inside runbook command scripts.

❌ **Ambiguous Remediations**: Writing vague troubleshooting steps like "Fix the index issue" instead of documenting the exact SQL commands needed to rebuild database indexes.

---

# Production Checklist

- [ ] Every repository contains a `docs/ops/RUNBOOK.md` file.
- [ ] Contact details and escalation paths are current.
- [ ] Trouble tickets link directly to correct runbooks.
- [ ] Runbooks contain copy-pasteable shell commands.
- [ ] Staging tests run runbook commands to confirm accuracy.

---

# Success Criteria

The Runbook program is successful when:
- On-call engineers can acknowledge and resolve common service failures within SLA windows.
- Incident logs confirm that developers copy-paste and execute runbook commands successfully.
- Game Day simulations verify that runbooks provide correct mitigation paths.

---

# Document Status

**Document:** NES-908 — Runbooks & Playbooks
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-909 — Incident Post-Mortems**
