---
document_id: LAW-009
title: Code Quality
subtitle: Code quality gates are enforced by CI — no exceptions, no bypasses
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-008 Performance
next_document: LAW-010 Architecture Compliance
---

# LAW-009 — Code Quality

> **"Quality is not negotiable. Low-quality code is not faster to ship — it is slower to fix, harder to extend, and more expensive to operate."**

---

## Law Statement

**All code submitted to the NeelStack codebase MUST pass automated quality gates before merging. Manual bypasses of CI quality checks are prohibited without explicit CTO approval documented in writing.**

---

## Code Quality Standards

### Python (Backend)

| Tool | Purpose | Threshold |
|---|---|---|
| `ruff` | Linting + import sorting | Zero warnings |
| `mypy` | Type checking (strict mode) | Zero errors |
| `black` | Code formatting | Auto-formatted |
| `pytest --cov` | Test coverage | ≥ 80% |
| `bandit` | Security static analysis | Zero HIGH findings |
| `radon` | Cyclomatic complexity | < 10 per function |

### TypeScript / JavaScript (Frontend)

| Tool | Purpose | Threshold |
|---|---|---|
| `eslint` | Linting | Zero errors |
| `prettier` | Code formatting | Auto-formatted |
| `tsc --noEmit` | Type checking | Zero errors |
| `jest --coverage` | Test coverage | ≥ 70% |

---

## Code Review Standards

All PRs must be reviewed by at least **one other engineer** before merging. Reviewers are responsible for:
1. Logic correctness
2. Security implications
3. Performance implications
4. Adherence to domain ownership rules (LAW-002)
5. Test completeness (LAW-006)

See NES-000 Engineering Handbook — Code Review Standards for the complete review checklist.

---

## Complexity Limits

| Metric | Limit | Rationale |
|---|---|---|
| Function length | ≤ 50 lines | Functions should do one thing |
| File length | ≤ 500 lines | Files should have single responsibility |
| Cyclomatic complexity | ≤ 10 | More than 10 paths = needs refactoring |
| Nesting depth | ≤ 4 levels | Deep nesting is a design smell |

---

## Technical Debt Policy

- Technical debt must be captured as GitHub Issues tagged `tech-debt`.
- No new feature may be built on top of unaddressed P1 technical debt.
- Monthly tech debt review in the Architecture Review Board (NES-1103).
- Maximum outstanding P1 tech debt: 0 items.
- P2 tech debt items must be resolved within 90 days.

---

## Anti-Patterns

❌ Disabling linting rules with `# noqa`, `// eslint-disable` without a documented reason.  
❌ Committing directly to `main` or `dev` without PR.  
❌ "I'll clean it up later" — PRs with TODO comments for core logic are rejected.  
❌ Copying code instead of extracting shared utilities.

---

## Related Standards

- NES-004 — Engineering Culture
- NES-800 — QA Principles
- NES-1101 — Technical Debt
- LAW-006 — Testing

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
