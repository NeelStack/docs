---
document_id: NSC-001
title: Pull Request Checklist
subtitle: Mandatory checklist for every pull request submitted to NeelStack repositories
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Engineering Leadership
document_type: Checklist
---

# NSC-001 — Pull Request Checklist

Every PR author must complete this checklist before requesting review. Every reviewer must verify these items before approving.

---

## Code Quality
- [ ] Code follows the language-specific style guide (Python: ruff/black/mypy | TypeScript: eslint/prettier/tsc)
- [ ] No linting errors or type errors (CI must be green)
- [ ] No `TODO` comments left for critical logic (non-critical TODOs have linked GitHub Issues)
- [ ] No commented-out code blocks
- [ ] Functions are < 50 lines, cyclomatic complexity < 10

## Testing
- [ ] New code has unit tests
- [ ] Integration tests added/updated for API endpoint changes
- [ ] All existing tests pass
- [ ] No tests skipped without documented reason
- [ ] Coverage did not decrease (CI enforces threshold)

## Security (LAW-007)
- [ ] No secrets, credentials, or API keys in code
- [ ] Input validation added for all user-facing parameters
- [ ] SQL queries use parameterized statements (no string concatenation)
- [ ] Auth and authorization checks in place for new endpoints

## Architecture (LAW-010)
- [ ] Business logic is in the domain layer (not in controllers or DB)
- [ ] No cross-domain direct DB access (only via events or APIs)
- [ ] Layer boundaries respected (no infrastructure imports in domain)

## Documentation (LAW-005)
- [ ] API documentation updated (OpenAPI/README) if endpoints changed
- [ ] ADR created if an architectural decision was made
- [ ] CHANGELOG updated if this is a user-facing change

## Performance (LAW-008)
- [ ] New DB queries have been EXPLAIN ANALYZED
- [ ] No N+1 queries introduced
- [ ] New expensive operations are async or backgrounded

## PR Hygiene
- [ ] PR title follows Conventional Commits format (`feat:`, `fix:`, `chore:`)
- [ ] PR description explains What, Why, and How
- [ ] Linked to GitHub Issue that this resolves
- [ ] Appropriate labels applied (bug, feature, chore, docs)

---

*Failure to complete this checklist may result in PR rejection by reviewers.*
