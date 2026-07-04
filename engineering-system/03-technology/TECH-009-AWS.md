---
document_id: TECH-009
title: AWS Standard
subtitle: AWS is the primary cloud provider for all NeelStack production infrastructure
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-008 OpenSearch
next_document: TECH-010 Docker
---

# TECH-009 — AWS Standard

---

## Primary Cloud Provider

**Amazon Web Services (AWS)** is the primary cloud provider. Azure and GCP are approved for specific workloads (see TECH-013).

## Approved AWS Services

| Service | Purpose |
|---|---|
| **EKS** | Kubernetes cluster hosting |
| **RDS (PostgreSQL)** | Managed database (non-critical) |
| **ElastiCache** | Managed Redis |
| **S3** | Object storage |
| **CloudFront** | CDN |
| **SES** | Transactional email |
| **SNS/SQS** | Messaging (where not using Kafka/RabbitMQ) |
| **Secrets Manager** | Secrets storage |
| **IAM** | Identity & access management |
| **VPC** | Network isolation |
| **Route 53** | DNS management |
| **ACM** | SSL/TLS certificate management |
| **CloudWatch** | AWS-native monitoring |

## Tagging Policy

Every AWS resource MUST have these tags:

```hcl
tags = {
  Environment = "production" # or staging, development
  Product     = "eduos"      # product name
  Team        = "backend"    # owning team
  CostCenter  = "engineering"
  ManagedBy   = "terraform"
}
```

Untagged resources are automatically flagged for review and may be terminated.

## Region Policy

- **Primary**: `ap-south-1` (Mumbai) — India-first products
- **DR**: `ap-southeast-1` (Singapore)
- Global products: Add `us-east-1` as tertiary

## Related Standards

- NES-509 — AWS Standards
- NES-503 — Terraform
- NES-515 — Infrastructure Security
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
