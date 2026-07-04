---
document_id: NES-1408
title: AWS Architecture
subtitle: Enterprise AWS Infrastructure & Landing Zone Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Reference Implementation
parent_document: NES-1407 — Kubernetes Architecture.md
next_document: NES-1409 — Azure Architecture.md
---

# NES-1408 — AWS Architecture

> **"Cloud architecture requires structured separation. This reference blueprint details our AWS VPC organization, EKS clusters, and secure storage networks."**

---

# Executive Summary

To operate a highly available, secure SaaS platform on AWS, we must enforce a structured infrastructure footprint.

This document establishes the official **NeelStack AWS Infrastructure Architecture** blueprint.

It defines our VPC configuration, landing zones, routing tables, compute node placement, database networks, and S3 secure bucket structures.

---

# Purpose

This standard defines:

- Unified AWS VPC and Routing Architecture Map
- Subnet Segmentation (Public, Private, Database Isolated)
- IAM Roles for Service Accounts (IRSA)
- Database Multi-AZ and Storage Configurations

---

# AWS Architecture Map

The AWS Architecture organizes resources into secure availability zones:

```text
  AWS Cloud Region (Multi-AZ active)
  ┌─────────────────────────────────────────────────────────────┐
  │  VPC Boundary (10.0.0.0/16)                                 │
  │                                                             │
  │  Public Subnets (NAT Gateway, ALB Ingress)                  │
  │  ├── Zone A (10.0.1.0/24)                                   │
  │  └── Zone B (10.0.2.0/24)                                   │
  │                                                             │
  │  Private Subnets (EKS Compute, App Pods)                    │
  │  ├── Zone A (10.0.10.0/24)                                  │
  │  └── Zone B (10.0.20.0/24)                                  │
  │                                                             │
  │  Database Isolated Subnets (RDS Postgres, Redis)            │
  │  ├── Zone A (10.0.100.0/24)                                 │
  │  └── Zone B (10.0.200.0/24) ──► RDS Multi-AZ sync           │
  └─────────────────────────────────────────────────────────────┘
```

---

# Subnet Segmentation & Security Groups

Maintain network isolation across subnets:

- **Public Subnets**: Host ALB instances, Cloudflare endpoints, and internet-facing NAT Gateways. Direct compute host deployment is prohibited.
- **Private Subnets**: Host EKS compute nodes. Pods route outbound traffic through NAT Gateways in public subnets.
- **Database Isolated Subnets**: Host RDS database instances. Enforce security groups that permit ingress connections *only* from EKS compute security groups.

---

# IAM Roles for Service Accounts (IRSA)

Secure application permissions on AWS:

- **OIDC Federation**: Configure OIDC federation between EKS and AWS IAM.
- **Least Privilege**: Map Kubernetes service accounts to specific AWS IAM roles (IRSA). Pods acquire temporary IAM credentials dynamically—hardcoded AWS access keys are prohibited.

---

# RDS Multi-AZ & S3 Storage Settings

- **Multi-AZ Databases**: Enable Multi-AZ on production RDS instances to ensure automated failover across availability zones.
- **Secure S3 Buckets**: Enforce SSE-KMS storage encryption, block public access, and enable versioning on all S3 buckets.

---

# Anti-Patterns

❌ **Direct Public DB Routing**: Placing RDS PostgreSQL instances in public subnets with public IP routes, exposing databases.

❌ **Shared Dev-Prod AWS Accounts**: Hosting sandbox testing compute nodes in the production AWS account workspace.

❌ **Exposing AWS Root Keys**: Storing root AWS credential keys in local settings files or code commits.

---

# Production Checklist

- [ ] VPC subnets match the architecture blueprint.
- [ ] Security groups restrict database ingress routes.
- [ ] IRSA OIDC federation is operational.
- [ ] RDS instances use active Multi-AZ failovers.
- [ ] S3 buckets block public access.

---

# Success Criteria

The AWS Infrastructure Architecture is successful when:
- Deployments scale automatically across availability zones.
- Database systems remain isolated from direct public routing.
- S3 storage complies with envelope encryption standards.

---

# Document Status

**Document:** NES-1408 — AWS Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1409 — Azure Architecture.md**
