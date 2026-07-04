---
document_id: ADR-002
title: PostgreSQL as Primary Database
status: Accepted
date: 2026-07-04
deciders: CTO, Chief Architect, Data Lead
consulted: Backend Engineering Team
informed: All Engineering
---

# ADR-002 — PostgreSQL as Primary Database

## Status

**Accepted** — In effect as of 2026-07-04

## Context

NeelStack requires a primary relational database supporting:
- ACID transactions for financial and enrollment data
- Multi-tenant row-level security
- JSON/JSONB for flexible schema evolution
- Vector embeddings for AI features (pgvector)
- Full-text search capability
- Cloud-managed options on AWS

## Decision

**We will use PostgreSQL 16+** as the primary relational database for all NeelStack services.

## Consequences

### Positive
- ACID compliance for billing and enrollment correctness
- `pgvector` extension enables AI embedding storage without a separate vector database
- Row-Level Security enables tenant isolation at the database layer
- JSONB enables schema flexibility without schema migrations for metadata
- AWS RDS and Aurora PostgreSQL provide managed options
- Excellent SQLAlchemy and Alembic support

### Negative
- Not ideal for time-series data at scale (use TimescaleDB for that)
- Not ideal for graph data (use Neo4j for complex relationships)
- Requires careful index management at scale

## Alternatives Considered

| Alternative | Rejected Reason |
|---|---|
| MySQL | Weaker JSONB support, no pgvector, weaker RLS |
| MongoDB | No ACID transactions across documents, harder to enforce schema |
| CockroachDB | Additional complexity, cost premium |
| DynamoDB | NoSQL — loses relational integrity for complex domain models |

## Related Standards

- NES-207 — PostgreSQL Standards
- TECH-005 — PostgreSQL Standard
- NES-206 — Data Architecture
