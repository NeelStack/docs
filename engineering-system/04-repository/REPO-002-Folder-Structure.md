---
document_id: REPO-002
title: Folder Structure Standard
subtitle: Standard folder structure for all NeelStack product repositories
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Annual
document_type: Repository Standard
parent_document: REPO-001 Monorepo
next_document: REPO-003 Package Structure
---

# REPO-002 — Folder Structure Standard

---

## Backend (FastAPI) Folder Structure

```
service-name/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/       # Route handlers (controllers)
│   │       └── dependencies/ # FastAPI dependencies
│   ├── core/
│   │   ├── config.py         # Settings (pydantic-settings)
│   │   ├── security.py       # Auth utilities
│   │   └── dependencies.py   # Global dependencies
│   ├── domain/
│   │   ├── entities/         # Domain entities
│   │   ├── services/         # Business logic
│   │   ├── repositories/     # Repository interfaces (ABC)
│   │   └── events/           # Domain events
│   ├── infrastructure/
│   │   ├── database/         # SQLAlchemy models + repos
│   │   ├── cache/            # Redis adapters
│   │   ├── messaging/        # Queue producers/consumers
│   │   └── external/         # Third-party API clients
│   ├── schemas/              # Pydantic request/response models
│   └── main.py               # App factory
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── alembic/                  # Database migrations
├── pyproject.toml
├── Dockerfile
└── README.md
```

## Frontend (Next.js) Folder Structure

```
web-app/
├── app/                      # Next.js App Router
│   ├── (auth)/               # Auth routes
│   ├── (dashboard)/          # Dashboard routes
│   ├── api/                  # API routes
│   ├── globals.css
│   └── layout.tsx
├── components/
│   ├── ui/                   # Primitive components (Button, Input)
│   ├── features/             # Feature-specific components
│   └── layouts/              # Page layout components
├── lib/
│   ├── api/                  # API client
│   ├── hooks/                # React hooks
│   ├── utils/                # Utility functions
│   └── validations/          # Zod schemas
├── stores/                   # Zustand stores
├── types/                    # TypeScript type definitions
├── public/                   # Static assets
└── tests/
```

## Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Files | `kebab-case` | `user-service.py` |
| Classes | `PascalCase` | `UserService` |
| Functions | `snake_case` (PY), `camelCase` (TS) | `get_user()`, `getUser()` |
| Constants | `SCREAMING_SNAKE` | `MAX_RETRY_COUNT` |
| Components | `PascalCase` | `UserProfileCard.tsx` |

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
