---
document_id: NES-1417
title: Infrastructure Maps
subtitle: Enterprise Infrastructure Provisioning & Terraform Resource Map
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Reference Implementation
parent_document: NES-1416 — CI-CD Pipelines.md
next_document: NES-1418 — Database ERDs.md
---

# NES-1417 — Infrastructure Maps

> **"Infrastructure must be defined as code. We map our Terraform module structures, cloud resource dependencies, and state files using Infrastructure maps."**

---

# Executive Summary

To scale and manage cloud infrastructure reliably across multiple accounts and regions, platform teams must maintain a clear blueprint of resource dependencies and Terraform configurations.

If we provision resources manually via cloud consoles, configuration drift and environment discrepancies will occur.

We mandate the use of **Infrastructure Maps** to guide IaC development.

This standard establishes our Terraform module organization, resource dependency trees, and state file management rules.

---

# Purpose

This standard defines:

- Infrastructure Map Principles
- Terraform Module Structures and Layouts
- Resource Dependency Trees
- State Locking and KMS Configurations

---

# Infrastructure Map Specification

Infrastructure maps document how Terraform modules and resources are organized:

```text
  terraform/
  ├── environments/            # Environment configurations
  │   ├── staging/             # Staging specific overrides (values)
  │   └── production/          # Production specific overrides (values)
  │
  ├── modules/                 # Reusable infrastructure blocks
  │   ├── vpc/                 # VPC and subnet segmentation scripts
  │   ├── eks/                 # EKS cluster and node group scripts
  │   └── database/            # RDS Postgres and Redis cache setups
  │
  └── global/                  # Global resources (Route53, S3 buckets)
```

---

# Resource Dependency & Provisioning

Maintain structured resource provisioning order:

- **Compute Dependencies**: Ensure network VPC resources are provisioned and active before attempting to initialize EKS clusters or RDS database instances.
- **Resource Tagging**: Enforce a unified tagging strategy (e.g. `Environment`, `Owner`, `Project`) across all provisioned cloud resources to support cost tracking.

---

# State File Locking & Encryption

- **State Storage**: Store Terraform state files in a secure, centralized Amazon S3 bucket.
- **Locking Configuration**: Configure DynamoDB state locking to prevent concurrent state updates. Enforce KMS encryption on all state files to protect resource data.

---

# Anti-Patterns

❌ **Hardcoded Infrastructure Credentials**: Storing provider passwords or keys inside Terraform code files, risking credentials leaks.

❌ **Excluding Terraform State Locks**: Running Terraform commands without active DynamoDB state locks, risking state file corruption.

❌ **Manual Console Changes**: Modifying cloud resources directly via console dashboards, introducing configuration drift.

---

# Production Checklist

- [ ] Terraform modules match the infrastructure map layout.
- [ ] Centralized S3 state storage is active with KMS encryption.
- [ ] DynamoDB state locking configurations are verified.
- [ ] Cost allocation tags are applied to all resources.
- [ ] Git repositories exclude sensitive terraform variables.

---

# Success Criteria

The Infrastructure Map standard is successful when:
- Teams can provision duplicate environments in under 15 minutes.
- Cloud resource dependencies are documented and clean.
- Code review processes flag and block configuration drifts.

---

# Document Status

**Document:** NES-1417 — Infrastructure Maps
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1418 — Database ERDs.md**
