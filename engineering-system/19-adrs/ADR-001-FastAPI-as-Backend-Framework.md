---
document_id: ADR-001
title: FastAPI as Primary Backend Framework
status: Accepted
date: 2026-07-04
deciders: CTO, Chief Architect, Backend Lead
consulted: Backend Engineering Team
informed: All Engineering
supersedes: N/A
---

# ADR-001 — FastAPI as Primary Backend Framework

## Status

**Accepted** — In effect as of 2026-07-04

## Context

NeelStack requires a Python backend framework that supports:
- High-concurrency async I/O for AI workloads
- Auto-generated OpenAPI documentation
- Strong type safety with Pydantic
- Fast development velocity
- Native async support for database and HTTP clients

Candidates evaluated:
1. **FastAPI** — Async-native, Pydantic v2, auto OpenAPI
2. **Django REST Framework** — Mature, sync-first (async support added later)
3. **Flask** — Lightweight, but requires many extensions for production use
4. **Litestar** — FastAPI alternative, newer

## Decision

**We will use FastAPI** as the primary backend framework for all NeelStack services.

## Consequences

### Positive
- Native `async/await` throughout the stack enables high-concurrency AI features
- Pydantic v2 provides strict type validation at the API boundary
- Automatic OpenAPI generation reduces documentation burden
- Strong Python ecosystem compatibility (LangChain, SQLAlchemy, Celery)
- Developer productivity: clear dependency injection system

### Negative
- Smaller ecosystem vs Django for admin interfaces (use separate admin service)
- Less opinionated than Django — requires more architectural discipline
- Django ORM not available (mitigated by SQLAlchemy)

## Alternatives Considered

| Alternative | Rejected Reason |
|---|---|
| Django REST Framework | Sync-first design creates blocking issues for AI workloads |
| Flask | Too minimal — every production feature must be added manually |
| Litestar | Excellent but smaller community, less ecosystem maturity |

## Related Standards

- NES-201 — FastAPI Architecture
- TECH-004 — FastAPI Standard
- NES-200 — Python Engineering Standards
