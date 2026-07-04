---
document_id: ADR-005
title: AWS as Primary Cloud Provider
status: Accepted
date: 2026-07-04
deciders: CTO, Chief Architect, Platform Lead
consulted: Platform Engineering Team
informed: All Engineering
---

# ADR-005 — AWS as Primary Cloud Provider

## Status

**Accepted** — In effect as of 2026-07-04

## Context

NeelStack requires a cloud provider for hosting all production infrastructure. Key requirements:
- India region availability (data residency for government products)
- Managed Kubernetes (EKS)
- Managed PostgreSQL (RDS)
- Strong compliance certifications (SOC2, ISO 27001)
- Competitive pricing for India market

## Decision

**We will use Amazon Web Services (AWS) as the primary cloud provider**, with:
- **Primary region**: `ap-south-1` (Mumbai) for India data residency
- **DR region**: `ap-southeast-1` (Singapore)

Azure and GCP remain approved for specific workloads (AI APIs, analytics) but not for primary infrastructure.

## Consequences

### Positive
- `ap-south-1` (Mumbai) provides <5ms latency for Indian users
- AWS has the strongest enterprise compliance certifications
- EKS, RDS, ElastiCache, S3, SES — all needed services available
- Largest ecosystem of managed services
- Government cloud certification (AWS GovCloud equivalent available)

### Negative
- Vendor lock-in risk (mitigated by Terraform IaC and Kubernetes portability)
- Higher egress costs vs some competitors
- AWS console complexity requires dedicated platform expertise

## Related Standards

- NES-509 — AWS Standards
- TECH-009 — AWS Standard
- NES-503 — Terraform
- NES-519 — Disaster Recovery
