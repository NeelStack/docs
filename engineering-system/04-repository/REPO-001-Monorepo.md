---
document_id: REPO-001
title: Monorepo Architecture
subtitle: NeelStack uses a monorepo structure — all products and services in one repository per domain
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Annual
document_type: Repository Standard
next_document: REPO-002 Folder Structure
---

# REPO-001 — Monorepo Architecture

> **"A well-organized monorepo is not a dumping ground — it is an intentional structure that enables fast, safe, and collaborative development."**

---

## Monorepo Strategy

NeelStack uses a **multi-repo strategy with monorepo patterns within each product domain**:

| Repository | Contents |
|---|---|
| `NeelStack/docs` | Engineering standards and documentation |
| `NeelStack/platform` | Shared infrastructure, Kubernetes configs, Terraform |
| `NeelStack/eduos` | EduOS product (frontend + backend) |
| `NeelStack/toolvines` | Toolvines product |
| `NeelStack/dhruvaos` | DhruvaOS product |
| `NeelStack/shared-libs` | Shared Python/TypeScript libraries |

---

## Monorepo Tool

**Turborepo** is the approved monorepo build system for JavaScript/TypeScript monorepos.

```json
// turbo.json
{
  "pipeline": {
    "build": { "dependsOn": ["^build"], "outputs": [".next/**", "dist/**"] },
    "test": { "dependsOn": ["^build"] },
    "lint": {}
  }
}
```

## Workspace Structure (within a product repo)

```
product-repo/
├── apps/
│   ├── web/          # Next.js frontend
│   ├── mobile/       # React Native app
│   └── api/          # FastAPI backend
├── packages/
│   ├── ui/           # Shared design system
│   ├── types/        # Shared TypeScript types
│   └── config/       # Shared configurations
├── infra/            # Terraform / K8s manifests
└── docs/             # Product-specific documentation
```

## Branch Strategy

- `main` — production-ready code
- `dev` — integration branch
- `feature/*` — feature branches (from dev)
- `hotfix/*` — production hotfixes (from main)
- `release/*` — release preparation branches

## Related Standards

- NES-102 — Monorepo Architecture
- REPO-002 — Folder Structure
- REPO-007 — Versioning

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
