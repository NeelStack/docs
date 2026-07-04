---
document_id: REPO-005
title: Import Rules
subtitle: Import organization and layer boundary rules for all NeelStack codebases
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Annual
document_type: Repository Standard
parent_document: REPO-004 Dependency Rules
next_document: REPO-006 Code Ownership
---

# REPO-005 — Import Rules

---

## Python Import Order

All Python files follow **PEP 8** import ordering, enforced by `ruff`:

```python
# 1. Standard library imports
import os
import uuid
from typing import Optional

# 2. Third-party imports
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# 3. Local application imports
from app.domain.services import EnrollmentService
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
```

`ruff` enforces this automatically. No manual sorting required.

## TypeScript Import Order

```typescript
// 1. Node built-ins
import path from 'path'

// 2. External packages
import { z } from 'zod'
import { useQuery } from '@tanstack/react-query'

// 3. Internal packages (monorepo)
import { Button } from '@neelstack/ui'

// 4. Relative imports (closest first)
import { UserService } from '../services/user-service'
import type { User } from './types'
```

Enforced by `eslint-plugin-import` with `import/order` rule.

## Layer Boundary Import Rules

The following cross-layer imports are **PROHIBITED** and enforced by CI:

```
# ❌ Domain importing from Infrastructure
from app.infrastructure.database.models import UserModel  # in domain/

# ❌ Presentation importing Domain directly
from app.domain.services import UserService  # in api/routes/ — use Application layer

# ✅ Correct: Application layer mediates
from app.domain.services import UserService  # in app/application/use_cases/
```

## Absolute vs Relative Imports

| Language | Rule |
|---|---|
| Python | Always use absolute imports from project root |
| TypeScript | Use path aliases (`@/components`, `@/lib`) for deep imports |

## Import Aliases (TypeScript)

Configure in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./components/*"],
      "@/lib/*": ["./lib/*"]
    }
  }
}
```

## Related Standards

- LAW-010 — Architecture Compliance
- NES-104 — Clean Architecture
- REPO-004 — Dependency Rules

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
