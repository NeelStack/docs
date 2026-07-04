---
document_id: NES-509
title: AWS
subtitle: Enterprise AWS Cloud Architecture, IAM, EKS & Storage Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-508 Cloudflare
next_document: NES-510 Multi-Cloud (Azure & GCP)
---

# NES-509 — AWS

> **"AWS is the primary host for the NeelStack platform. We manage cloud accounts using Landing Zones, strict IAM least privilege, and managed services."**

---

# Executive Summary

Amazon Web Services (AWS) hosts our core compute nodes, relational databases, event streams, and file assets.

Misconfigured AWS accounts cause resource leakage, multi-million dollar billing mistakes, security breaches, and availability issues.

This standard establishes our AWS account hierarchy, IAM security permissions, database management, and compute standards.

---

# Purpose

This standard defines:

- AWS Organizations and Landing Zones
- IAM Least Privilege and Role-Based Access Control
- Compute Standards (Elastic Kubernetes Service - EKS)
- Database and Cache Storage (RDS, ElastiCache)
- Asset Storage Security (S3)

---

# AWS Organizations & Account Structure

To limit impact zones, we isolate workloads across separate AWS accounts using **AWS Organizations**:

```text
               AWS Organizations (Root)
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
Core Services        Workloads          Sandbox
  (Shared Infra,       ├── Development    (R&D, Temp
   DNS, CI Runner)     ├── Staging         workspace)
                       └── Production
```

- **Production Account**: Completely isolated. No database or S3 resource can be read from other accounts without encrypted cross-account roles.

---

# IAM & Access Control

Access control must follow the **principle of least privilege**.

- **No Root Usage**: Root accounts are restricted to registration only. Access is locked with hardware MFA.
- **SSO Access**: Enable **AWS IAM Identity Center (SSO)**. Developers assume temporary session roles (max 4 hours) rather than generating static access keys.
- **Service IAM Roles (IRSA)**: EKS Pods must authenticate to S3 or RDS using IAM Roles for Service Accounts (IRSA) via OIDC tokens. Do not pass AWS access keys as environment variables.

---

# Compute Standard (EKS)

We run our microservice containers inside **Amazon Elastic Kubernetes Service (EKS)**.

- **Fargate vs. Managed Nodes**:
  - Use EKS Managed Node Groups (utilizing Bottlerocket OS for security hardening) for heavy workloads like Kafka and vector databases.
  - Use AWS Fargate for transient web tasks or APIs that scale dynamically.
- **VPC Bindings**: Nodes must reside in private subnets. Only the Load Balancer targets (ALB/NLB) are exposed to public subnets.

---

# Database & Cache Storage (RDS, ElastiCache)

Database management requires automation and redundancy.

- **Relational**: Use **Amazon RDS (PostgreSQL)** configured with Multi-AZ (Automatic failover) for production.
- **Cache**: Use **Amazon ElastiCache (Redis)**.
- **Encryption**: Enable Storage Encryption at Rest using AWS Key Management Service (KMS) with Customer Managed Keys (CMKs).

---

# Asset Storage (S3 Security)

Amazon S3 buckets store user assets, uploads, and logs.

- **Block Public Access**: Enable "Block Public Access" at the bucket level.
- **Encryption**: Enforce SSE-KMS encryption for all uploads.
- **Lifecycle Policies**: Move logs and older records to Glacier Deep Archive after 90 days to control storage costs.
- **Presigned URLs**: Access to S3 resources must pass through secure backend-generated Presigned URLs with tight expiration windows (max 15 minutes).

---

# Anti-Patterns

❌ **Using Default VPC**: Deploying production instances inside the default AWS VPC.

❌ **Hardcoded IAM Access Keys**: Creating local IAM users (e.g. `s3-upload-user`) and hardcoding access keys in environment files. Always use temporary OIDC session roles.

❌ **Open S3 Buckets**: Configuring open bucket policies to share static images. Serve images through Cloudfront CDN with Origin Access Control (OAC) instead.

---

# Production Checklist

- [ ] Multi-AZ configuration is active on all production RDS instances.
- [ ] OIDC provider is configured inside EKS for IRSA authentication.
- [ ] AWS SSO is configured with active MFA policies.
- [ ] "Block Public Access" is enabled on all S3 buckets.
- [ ] KMS encryption is verified on all RDS and S3 resources.

---

# Success Criteria

The AWS architecture is successful when:
- Failures of a single AWS availability zone (AZ) trigger automatic sub-second node failovers.
- No static AWS developer access key exists in production configurations.
- Annual AWS security audit reports zero active High severity findings.

---

# Document Status

**Document:** NES-509 — AWS
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-510 — Multi-Cloud (Azure & GCP)**
