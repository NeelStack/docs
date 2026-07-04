---
document_id: TECH-005
title: PostgreSQL Standard
subtitle: PostgreSQL is the primary relational database for all NeelStack services
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Data Platform Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-004 FastAPI
next_document: TECH-006 Redis
---

# TECH-005 — PostgreSQL Standard

---

## Approved Version

**PostgreSQL 16+** — always use the latest stable major version.

## When to Use PostgreSQL

- All transactional data
- Domain entities (users, tenants, orders)
- Audit logs
- Multi-tenant data with row-level security
- Vector embeddings (via `pgvector`)

## When NOT to Use PostgreSQL

| Use Case | Use Instead |
|---|---|
| Session data | Redis |
| Full-text search at scale | OpenSearch |
| Time-series metrics | TimescaleDB / InfluxDB |
| Ephemeral cache | Redis |

## Multi-Tenant Row-Level Security

```sql
-- Enable RLS on every tenant-scoped table
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON enrollments
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Required Practices

- All schema changes via **Alembic migrations** — no manual DDL in production
- Every table has `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- Every table has `created_at TIMESTAMPTZ DEFAULT NOW()` and `updated_at TIMESTAMPTZ`
- All foreign keys have explicit indexes
- EXPLAIN ANALYZE run on all new queries before production

## Extensions

| Extension | Purpose |
|---|---|
| `pgvector` | AI embeddings |
| `pg_trgm` | Fuzzy text search |
| `uuid-ossp` | UUID generation |
| `pg_stat_statements` | Query performance tracking |

## Related Standards

- NES-207 — PostgreSQL Standards
- NES-206 — Data Architecture
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
