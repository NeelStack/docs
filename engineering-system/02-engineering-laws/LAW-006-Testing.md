---
document_id: LAW-006
title: Testing
subtitle: No code ships to production without automated tests — coverage thresholds are enforced by CI
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-005 Documentation
next_document: LAW-007 Security
---

# LAW-006 — Testing

> **"Untested code is a bug that hasn't been found yet. Untested production systems are incidents waiting to happen."**

---

## Law Statement

**All production code MUST have automated tests. The CI pipeline MUST enforce minimum coverage thresholds. No code may be merged to main without passing the full test suite.**

---

## Coverage Requirements

| Layer | Minimum Coverage | Tool |
|---|---|---|
| Domain / Business Logic | **90%** | pytest / jest |
| Application Services | **80%** | pytest / jest |
| API Endpoints | **80%** | pytest-httpx / supertest |
| Frontend Components | **70%** | jest + React Testing Library |
| Infrastructure Adapters | **60%** | pytest with mocks |

---

## Test Pyramid

```
        ┌───────────┐
        │    E2E    │  ← Small number, high confidence (Playwright/Detox)
        ├───────────┤
        │Integration│  ← Service boundary tests
        ├───────────┤
        │   Unit    │  ← Fast, isolated, most numerous
        └───────────┘
```

**Rule**: The pyramid must not be inverted. More unit tests than integration tests. More integration tests than E2E tests.

---

## Testing Standards by Type

### Unit Tests
- Must be isolated (no real DB, no real HTTP calls)
- Use dependency injection to mock all external dependencies
- Run in < 5 minutes for the full suite
- Named: `test_<behavior>_when_<condition>_should_<expectation>`

### Integration Tests
- Test service boundaries (API → DB, Service → Queue)
- Use test containers or in-memory equivalents
- Clean up after each test (no shared state between tests)

### E2E Tests
- Cover critical user journeys only
- Run against a staging environment
- Must not depend on test ordering

---

## CI Enforcement

The GitHub Actions pipeline MUST:
1. Run `pytest` with `--cov` and fail if coverage drops below threshold
2. Run `jest --coverage` and fail if coverage drops below threshold
3. Block PR merge if any test fails
4. Report coverage delta on every PR

---

## Anti-Patterns

❌ Writing tests only after a bug is reported.  
❌ Mocking the thing under test.  
❌ Tests that always pass because they assert nothing meaningful.  
❌ Skipping tests in CI with `--no-cov` or `--ignore`.  
❌ 100% line coverage with 0% branch coverage.

---

## Related Standards

- NES-800 — QA Principles
- NES-801 — Test Strategy
- NES-802 — Unit Testing
- NES-803 — Integration Testing
- NES-804 — E2E Testing
- NES-312 — Frontend Testing Standards

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
