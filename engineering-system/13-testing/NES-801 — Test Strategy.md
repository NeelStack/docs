---
document_id: NES-801
title: Test Strategy
subtitle: Enterprise Release Environments, Testing Gates & Sanity Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Quality Assurance Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-800 QA Principles
next_document: NES-802 Unit Testing
---

# NES-801 — Test Strategy

> **"Code promotion requires environmental validation. We test logic in isolated sandbox, staging, and pre-production zones before production deployment."**

---

# Executive Summary

Deploying code modifications directly to production without testing in environments that match production configurations causes unexpected errors, database conflicts, and downtime.

We mandate a structured **Environment Promotion Lifecycle** across all NeelStack engineering processes.

This standard establishes our environment topologies (Sandbox, Staging, Production), verification gates, smoke test rules, and promotion criteria.

---

# Purpose

This standard defines:

- Isolated Testing Environments
- Release Gate Validation Rules
- Smoke, Regression, and Sanity Testing Criteria
- Environment Variables Separation
- Hotfix Promotion Exceptions Playbook

---

# Environment Promotion Lifecycle

Our code release path requires validation across three environment tiers:

```text
  Local Dev (Sandbox) ──►  Staging VPC (Test)  ──►  Pre-Production  ──►  Production
          │                       │                        │                 │
     Local mocks              Integration              Canary /           Public
    & SQLite databases        databases                Load Tests         Workloads
```

- **Sandbox Tier (Local)**: Runs on developer local machines. Uses mock data, local Docker containers, or SQLite data instances (NES-409).
- **Staging Tier (Staging)**: Deployed automatically on pull request merge. Runs in a dedicated Kubernetes namespace mimicking production sizing with anonymized transactional databases.
- **Production Tier**: Deployed only after pre-production smoke runs pass. Restricted to active customer queries.

---

# Release Gate Validation Rules

Promoting build versions through environment tiers requires passing explicit gates:

- **Unit Gate**: 100% of unit tests must compile and pass.
- **Security Gate**: Container vulnerabilities (Trivy scans) report zero critical findings.
- **Staging Smoke Gate**: Automated verification scripts (smoke runs validating logins, database connections, core endpoints) must execute cleanly in staging inside 3 minutes post-deploy.

---

# Smoke, Regression & Sanity Testing

Configure testing sweeps based on release scale:

- **Sanity Testing**: Run targeted check scripts following minor bug fixes to verify the patched component behaves correctly without running the entire regression test catalog.
- **Smoke Testing**: A lightweight test suite verifying core system accessibility (e.g. database online, web page assets load) executed immediately after deployments.
- **Regression Testing**: A comprehensive test suite validating all system functions, executed daily in staging and before all major production releases.

---

# Environment Variables Isolation

Never allow sandbox or staging containers to access production API keys or databases:

- **Secret Keys Isolation**: Keep credentials separated using AWS Secrets Manager instances bound to distinct AWS account limits (NES-509).
- **No Cross-Environment Writes**: Staging code must never write database rows or publish API messages to production systems.

---

# Anti-Patterns

❌ **Testing in Production**: Testing new feature options directly in production using "test accounts," risking database corruption or accidental emails to real users.

❌ **Shared Environment Databases**: Connecting staging and development containers to the same physical database instances, causing data overwrites and test failures.

❌ **Excluding Post-Deploy Smoke Checks**: Declaring deployments complete as soon as containers report "running" status in Kubernetes without verifying if the web server can actually resolve database queries.

---

# Production Checklist

- [ ] Isolated environments (Dev, Staging, Prod) are configured.
- [ ] Staging database uses anonymized data profiles.
- [ ] Post-deploy smoke test automation is active.
- [ ] Environment secrets use separate KMS namespaces.
- [ ] Release promotion policies require dual-approvals.

---

# Success Criteria

The Test Strategy program is successful when:
- 100% of code promotions pass automated environment smoke gates.
- Zero development or staging connection traces hit production databases.
- Regression runs catch feature incompatibilities in staging before release branches compile.

---

# Document Status

**Document:** NES-801 — Test Strategy
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-802 — Unit Testing**
