---
document_id: NES-904
title: Blue-Green Deployments
subtitle: Enterprise Blue-Green Deployments, ALB Routing & Schema Migration Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-903 Feature Flags
next_document: NES-905 Canary Releases
---

# NES-904 — Blue-Green Deployments

> **"Zero downtime requires parallel hosting. We switch traffic routing at the Load Balancer level and enforce backward-compatible database schemas."**

---

# Executive Summary

Traditional deployments require shutting down active services to launch new versions, which causes downtime.

Additionally, if a deployment fails, reversing changes can cause data loss if database tables were altered in a non-backward-compatible manner.

We mandate the use of **Blue-Green Deployments** for all core stateless applications.

This standard establishes our environment swapping configurations, ALB traffic routing rules, and database schema migrations (Expand & Contract pattern).

---

# Purpose

This standard defines:

- Blue-Green Environment Topologies
- Application Load Balancer (ALB) Routing Switches
- Backward-Compatible Database Migrations (Expand and Contract)
- Session Draining Configurations
- Rollback Execution Rules

---

# Blue-Green Topologies

We maintain two identical, isolated production environments:

- **Blue (Active)**: Currently serves production traffic.
- **Green (Stage)**: Receives the new deployment build. Runs validations in isolation.

```text
                        Public Traffic (ALB Ingress)
                                      │
                         (Route Switch - DNS / Target Group)
                                      │
                       ┌──────────────┴──────────────┐
                       ▼                             ▼
                [ Blue (Active) ]             [ Green (Stage) ]
                - Version 1.2.0               - Version 1.3.0
```

---

# ALB Routing Switches

The environment swap occurs at the Application Load Balancer (ALB) level using Target Groups:

- **Target Group Swap**: Swap traffic routing by updating the ALB listener target weight (e.g. Blue: 0%, Green: 100%).
- **DNS Swap (Alternative)**: For cross-region setups, update Cloudflare DNS CNAME pointers.

---

# Database Backward Compatibility (Expand & Contract)

Database schema migrations must remain compatible with both Blue and Green application versions. This is achieved using the **Expand and Contract** pattern:

- **Phase 1 (Expand)**: Modify the database to support the new version (e.g., add a column named `full_name`) while keeping the old columns active (e.g. `first_name`, `last_name`). Run database writes to duplicate data to both columns.
- **Phase 2 (Deploy)**: Deploy the Green application version, which reads and writes exclusively to the new columns.
- **Phase 3 (Contract)**: After verifying stable operations for 7 days, drop the old columns (`first_name`, `last_name`) from the database tables.

```text
  Expand Phase: Add new columns alongside old ones
  Deploy Phase: Swap traffic to Green application version
  Contract Phase: Drop old database columns safely
```

---

# Session Draining

To prevent active user transactions or file uploads from dropping during an environment swap:

- Enforce a **60-second Session Draining Timeout** on target groups.
- The load balancer routes new requests to the Green environment while permitting Blue nodes to finish processing active connections before shutdown.

---

# Anti-Patterns

❌ **Direct Column Renaming**: Renaming database columns (e.g. `name` to `first_name`) in a single migration script. This crashes the active Blue application version before the Green version is deployed.

❌ **Omitting Target Group Draining**: Shutting down Blue application pods immediately upon green activation, dropping active user sessions.

❌ **Running Shared Redis Sessions with Mismatched Schemas**: Changing session cache schemas in the Green version in a way that crashes the Blue version sharing the cache.

---

# Production Checklist

- [ ] Blue and Green Target Groups are initialized in AWS.
- [ ] Database migrations follow the Expand & Contract pattern.
- [ ] Target Group connection draining is set to 60 seconds.
- [ ] Routing updates are automated via Terraform scripts.
- [ ] Rollback validation scripts are verified.

---

# Success Criteria

The Blue-Green deployment model is successful when:
- Releases execute with zero downtime or user session terminations.
- Rollbacks can be executed in under 30 seconds by swapping target weights.
- Database changes support parallel versions during deployments.

---

# Document Status

**Document:** NES-904 — Blue-Green Deployments
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-905 — Canary Releases**
