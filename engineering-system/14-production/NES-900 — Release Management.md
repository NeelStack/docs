---
document_id: NES-900
title: Release Management
subtitle: Enterprise Release Management, Branch Promotion & Post-Deploy Gates
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-812 Reference Architecture
next_document: NES-901 Semantic Versioning
---

# NES-900 — Release Management

> **"Deployments are operational, releases are commercial. We decouple code changes from client visibility and validate health at every stage."**

---

# Executive Summary

Pushing code modifications to production databases and live user instances carries inherent operational risks.

A failed release can result in system downtime, broken client workflows, database integrity corruption, and immediate loss of revenue.

We mandate a structured **Release Management** lifecycle across all NeelStack products.

This standard outlines the deployment roles, release windows, branch promotion flows, and post-deployment validation loops.

---

# Purpose

This standard defines:

- Deployment vs. Release Decoupling
- Release Windows and Calendars
- Branch Promotion and Git Workflows
- Post-Deployment Validation (Smoke Tests)
- Deployment Roles and Accountability

---

# Decoupling Deployments from Releases

We enforce the separation of technical deployments from business releases:

- **Deployment**: The physical installation of a build container on production nodes (inactive to users, controlled via routing weights or hidden behind feature flags).
- **Release**: The activation of a new feature for public customer traffic.
- **Benefit**: Allows teams to deploy code during normal working hours and activate features dynamically when business indicators align, reducing risk.

---

# Release Windows & Calendars

To prevent coordination conflicts and preserve operational bandwidth:

- **Approved Deploy Windows**: Standard production deployments occur **Monday through Thursday between 9:00 AM and 4:00 PM**.
- **No-Deploy Windows**: Deployments are prohibited on Fridays, weekends, national holidays, or during major client operational periods (e.g., student exam weeks in EduOS), unless resolving a critical SEV-1 outage.

---

# Branch Promotion Workflow

We use a Git-based promotion path to push code through environments:

```text
  Feature Branch ──► Pull Request ──► main Branch (Dev/Staging)
                          │
                  Approval & CI passes
                          │
                          ▼
                 release/vX.Y.Z Branch (Pre-Prod)
                          │
                 Manual Smoke Validation
                          │
                          ▼
                 production Branch (Release)
```

- **Release Tagging**: Merges to the `production` branch automatically compile the release build and tag the repository with a semantic version number (NES-901).

---

# Post-Deployment Validation (Smoke Gates)

Immediately after container deployment to production hosts:

- **Automated Smoke Test**: Schedulers execute automated check scripts (validating database connections, health endpoints response statuses, static assets loads) in under 3 minutes.
- **Canary Monitor**: Monitor container metrics (error rates, CPU saturation) for 15 minutes before shifting 100% of user traffic to the new build.

---

# Anti-Patterns

❌ **Deploying on Friday Afternoon**: Pushing major platform updates right before weekends, which leaves operations teams short-staffed if outages occur.

❌ **Direct Merges to Production**: Overriding Git branch protection rules to merge changes directly into the `production` branch, bypassing CI/CD validation.

❌ **Excluding Post-Deploy Checks**: Verifying a release only by checking if containers report "Running" in Kubernetes without running end-to-end API validations.

---

# Production Checklist

- [ ] Release branch promotion rules are active in Git.
- [ ] Scheduled release windows are registered in the calendar.
- [ ] Post-deploy automated smoke scripts are verified.
- [ ] Feature flags are active for un-released code paths.
- [ ] Platform Operations Team signs off on the release manifest.

---

# Success Criteria

The Release Management program is successful when:
- Deployments execute with zero service downtime or customer disruption.
- Failed builds are identified and rolled back automatically in under 5 minutes.
- Release schedules remain predictable and synchronized across all product teams.

---

# Document Status

**Document:** NES-900 — Release Management
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-901 — Semantic Versioning**
