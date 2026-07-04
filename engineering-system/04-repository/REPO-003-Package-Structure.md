---
document_id: REPO-003
title: Package Structure Standard
subtitle: How Python and Node packages are organized and versioned within NeelStack repositories
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Annual
document_type: Repository Standard
parent_document: REPO-002 Folder Structure
next_document: REPO-004 Dependency Rules
---

# REPO-003 — Package Structure Standard

---

## Python Package Structure

Every Python service uses **pyproject.toml** (no setup.py, no requirements.txt alone):

```toml
[project]
name = "enrollment-service"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115.0",
  "pydantic>=2.5.0",
  "sqlalchemy>=2.0.0",
  "alembic>=1.13.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.3", "mypy>=1.8"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.mypy]
strict = true
python_version = "3.12"
```

## Node.js / TypeScript Package Structure

Every TypeScript package uses **package.json** with exact version pinning in monorepo:

```json
{
  "name": "@neelstack/ui",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit"
  },
  "peerDependencies": {
    "react": "^19.0.0"
  }
}
```

## Dependency Pinning Policy

| Environment | Pinning Strategy |
|---|---|
| Production | Exact version (`==` in Python, no `^` in Node) |
| Development | Minor version range acceptable |
| Shared libraries | Exact version |

## Private Package Registry

All internal shared packages are published to GitHub Packages:
- Python: `pip install --index-url https://pypi.pkg.github.com/NeelStack/ neelstack-core`
- Node: `@neelstack/*` packages from GitHub npm registry

## Related Standards

- REPO-004 — Dependency Rules
- REPO-001 — Monorepo Architecture

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
