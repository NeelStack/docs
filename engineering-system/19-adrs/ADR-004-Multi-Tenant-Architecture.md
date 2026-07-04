---
document_id: ADR-004
title: Multi-Tenant SaaS Architecture with Row-Level Security
status: Accepted
date: 2026-07-04
deciders: CTO, Chief Architect, Backend Lead
consulted: Security Team, Data Team
informed: All Engineering
---

# ADR-004 — Multi-Tenant SaaS Architecture

## Status

**Accepted** — In effect as of 2026-07-04

## Context

NeelStack products serve multiple organizations (schools, enterprises, government departments) from a single platform. The architecture must ensure complete data isolation between tenants while minimizing operational overhead.

Three tenancy models were considered:
1. **Silo**: Separate database per tenant
2. **Bridge**: Separate schema per tenant, shared database
3. **Pool**: Shared tables with `tenant_id` column isolation

## Decision

**We will use the Pool model (shared tables) with PostgreSQL Row-Level Security (RLS)** as the primary multi-tenancy strategy.

The `tenant_id` column is present in every tenant-scoped table. PostgreSQL RLS policies enforce that every query is scoped to the current tenant session.

## Consequences

### Positive
- Simple operational model — one database cluster to manage
- PostgreSQL RLS enforces isolation at the database engine level (not application level)
- Easy to add new tenants (no database provisioning required)
- Cross-tenant analytics possible by bypassing RLS at the data warehouse layer

### Negative
- Noisy neighbor risk — one tenant's heavy queries affect others (mitigated by connection pooling and query limits)
- Schema migrations affect all tenants simultaneously
- Very large tenants may require eventual migration to dedicated databases

## Mitigation

- Connection pooling via PgBouncer prevents connection exhaustion
- Resource quotas per tenant implemented at application layer
- Tenant isolation verified by automated integration tests on every PR

## Related Standards

- NES-205 — Multi-Tenancy Architecture
- NES-207 — PostgreSQL Standards (RLS section)
- NES-204 — Authorization (RBAC & Permissions)
