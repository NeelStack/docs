---
document_id: RFC-003
title: Multi-Tenant Data Isolation Model
status: Draft
date: 2026-07-04
author: Data Architecture Team
reviewers: Chief Architect, Security Lead, Data Lead
discussion_deadline: 2026-08-10
---

# RFC-003 — Multi-Tenant Data Isolation Model

## Summary

This RFC proposes formalizing the multi-tenant data isolation strategy across all NeelStack data stores — not just PostgreSQL, but also Redis, OpenSearch, S3, and Kafka.

## Current State

ADR-004 approved PostgreSQL Row-Level Security as the tenancy model for relational data. However, isolation in other data stores is inconsistent:
- Redis: Some services use `tenant_id` prefixes, some don't
- OpenSearch: Mix of shared and per-tenant indexes
- S3: Some services use shared buckets without tenant prefixes
- Kafka: Topics shared across tenants

## Proposal

Standardize isolation across all data stores:

### PostgreSQL (existing)
- Row-Level Security enforced via `tenant_id` column ✅

### Redis
- **Key isolation**: All keys MUST be prefixed with `{tenant_id}:`
- No shared keys without explicit tenant scope
- Redis DB per environment (dev/staging/prod), not per tenant

### OpenSearch
- **Index isolation**: Per-tenant indexes for all business data: `{product}-{entity}-{tenant_id}`
- Shared indexes acceptable ONLY for system/audit logs with `tenant_id` field filter

### S3
- **Bucket path isolation**: All objects at `s3://neelstack-{product}/{env}/{tenant_id}/{resource}/`
- No cross-tenant path traversal possible with this structure
- IAM bucket policies restrict service access to own prefix

### Kafka
- **Topic isolation**: Business events on per-tenant topics: `{product}.{domain}.{event}.{tenant_id}`
- High-volume tenants get dedicated consumer groups

## Migration Plan

Existing services must migrate to these standards by Q3 2026.

## Open Questions

1. Should we use OpenSearch Document-Level Security instead of index-per-tenant for cost optimization at scale?
2. What is the S3 cost implication of per-tenant prefixes vs per-tenant buckets?

## Related Standards

- NES-205 — Multi-Tenancy Architecture
- NES-208 — Redis Standards
- NES-210 — Search Architecture
- NES-209 — Object Storage Standards
- ADR-004 — Multi-Tenant Architecture
