---
document_id: TECH-004
title: FastAPI Standard
subtitle: FastAPI is the approved Python backend framework for all NeelStack services
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Backend Platform Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-003 React Native
next_document: TECH-005 PostgreSQL
---

# TECH-004 — FastAPI Standard

---

## Approved Version

**FastAPI 0.115+** with **Python 3.12+** and **Pydantic v2**

## Core Stack

| Package | Purpose | Required |
|---|---|---|
| `fastapi` | Web framework | ✅ |
| `pydantic` v2 | Data validation | ✅ |
| `sqlalchemy` 2.x | ORM | ✅ |
| `alembic` | DB migrations | ✅ |
| `httpx` | Async HTTP client | ✅ |
| `celery` | Background tasks | ✅ |
| `redis` | Cache + broker | ✅ |
| `pytest` | Testing | ✅ |
| `ruff` | Linting | ✅ |
| `mypy` | Type checking | ✅ |

## Service Structure

```
app/
├── api/v1/          # Versioned API routes
├── core/            # Config, security, dependencies
├── domain/          # Business logic (entities, services)
├── infrastructure/  # DB repos, external clients
├── schemas/         # Pydantic request/response schemas
└── main.py          # App entry point
tests/
├── unit/
├── integration/
└── e2e/
```

## Async First

All route handlers MUST be `async def`. Synchronous handlers block the event loop:

```python
# ✅ Correct
@router.get("/users/{user_id}")
async def get_user(user_id: UUID, service: UserService = Depends()):
    return await service.get_user(user_id)
```

## Related Standards

- NES-200 — Python Engineering Standards
- NES-201 — FastAPI Architecture
- NES-202 — API Design Standards
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
