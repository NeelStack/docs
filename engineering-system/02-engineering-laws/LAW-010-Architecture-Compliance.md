---
document_id: LAW-010
title: Architecture Compliance
subtitle: All code must comply with defined architectural boundaries — violations are blocking issues
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-009 Code Quality
next_document: NES-100 Architecture Principles
---

# LAW-010 — Architecture Compliance

> **"Architecture is only as strong as its enforcement. A diagram on the wall that nobody follows is a lie."**

---

## Law Statement

**All code must respect the architectural layer boundaries and domain ownership rules defined in the Engineering Constitution. Architecture violations are blocking issues that prevent merge. The Architecture Review Board is the final authority on all architectural decisions.**

---

## Architectural Layers (Clean Architecture)

```
┌─────────────────────────────────────┐
│         Presentation Layer          │  ← HTTP controllers, GraphQL resolvers
├─────────────────────────────────────┤
│         Application Layer           │  ← Use cases, application services
├─────────────────────────────────────┤
│           Domain Layer              │  ← Entities, aggregates, domain services
├─────────────────────────────────────┤
│        Infrastructure Layer         │  ← DB repos, external APIs, message queues
└─────────────────────────────────────┘
```

**Dependency Rule**: Dependencies flow inward only. Outer layers may depend on inner layers. Inner layers may NEVER depend on outer layers.

---

## Prohibited Dependencies

| From Layer | May NOT import from |
|---|---|
| Domain | Infrastructure, Application, Presentation |
| Application | Infrastructure, Presentation |
| Presentation | Domain (only via Application) |

---

## Automated Enforcement

Architecture compliance is enforced automatically:

```bash
# Python: import-linter checks in CI
lint-imports --config .importlinter

# TypeScript: eslint import boundaries
eslint --rule 'import/no-restricted-paths: error'
```

Any import that violates the dependency rule fails CI with a clear error message identifying the violating import.

---

## Architecture Review Board (ARB)

Any of the following require an ARB decision:
- Introducing a new external dependency (package/library)
- Introducing a new service or domain
- Changing an existing API contract
- Deviating from any standard in the Engineering Constitution
- Cross-domain data access patterns

ARB decisions are recorded as ADRs in `19-adrs/`. See NES-1103 — Architecture Review Board.

---

## Architecture Fitness Functions

Automated fitness tests run in CI to validate:
- Layer dependency directions
- Naming conventions (NES prefixes in docs)
- No circular dependencies between modules
- Domain boundary assertions

---

## Anti-Patterns

❌ "We'll refactor to the right architecture later." — Architecture debt compounds exponentially.  
❌ Direct infrastructure imports in domain classes.  
❌ Global singletons shared across domain boundaries.  
❌ Feature branches that skip ARB for new service introductions.

---

## Related Standards

- NES-100 — Architecture Principles
- NES-104 — Clean Architecture
- NES-110 — Architecture Governance
- NES-1103 — Architecture Review Board
- LAW-001 — Business Logic
- LAW-002 — Domain Ownership

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
