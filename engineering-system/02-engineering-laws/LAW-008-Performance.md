---
document_id: LAW-008
title: Performance
subtitle: Performance SLAs must be defined before development begins and validated before production
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-007 Security
next_document: LAW-009 Code Quality
---

# LAW-008 — Performance

> **"Performance is a feature. Slow software is broken software. Define your SLAs before you write your first line of code."**

---

## Law Statement

**Every service must have defined performance SLAs agreed upon before development begins. Performance regression tests must run in CI. No service may be deployed to production if it violates its defined SLA.**

---

## NeelStack Default SLA Targets

| API Type | p50 | p95 | p99 |
|---|---|---|---|
| Read (GET, cached) | < 50ms | < 100ms | < 200ms |
| Read (GET, uncached) | < 100ms | < 300ms | < 500ms |
| Write (POST, PUT) | < 200ms | < 500ms | < 1000ms |
| Search | < 200ms | < 500ms | < 800ms |
| AI / LLM | < 1s | < 3s | < 5s |
| File Upload | < 2s | < 5s | < 10s |

These are defaults. Teams may define stricter SLAs for their domain. Looser SLAs require ARB approval (NES-1103).

---

## Performance Design Principles

1. **Measure first**: Use APM data to identify actual bottlenecks before optimizing.
2. **Cache strategically**: Apply Redis caching to hot paths. Define TTL explicitly.
3. **Paginate always**: No endpoint returns an unbounded list. Default page size ≤ 100.
4. **Async for long operations**: Operations > 500ms should be async with job status polling.
5. **Database indexes**: Explain plans reviewed for all new queries before production.
6. **CDN for assets**: Static assets served via CDN (NES-511). Never from origin for static content.

---

## CI Performance Gates

```yaml
# Example: k6 load test in CI
k6 run --vus 100 --duration 30s load_test.js
# Fail if: p95 > 500ms OR error_rate > 0.1%
```

Load tests must run against staging before every major release.

---

## Capacity Planning

Before launch of any new service or major feature:
- Define expected request rate (RPS) at launch, 3 months, 12 months
- Provision resources for 2× expected peak
- Document scaling strategy (horizontal vs vertical)
- Define auto-scaling triggers

---

## Anti-Patterns

❌ N+1 queries — fetching related data in a loop.  
❌ Unbounded `SELECT *` queries.  
❌ Synchronous calls to third-party APIs in the request path (use queues).  
❌ In-memory sorting/filtering of large datasets.  
❌ "Premature optimization" used as an excuse to never optimize.

---

## Related Standards

- NES-805 — Performance Testing
- NES-806 — Load Testing
- NES-411 — Mobile Performance
- NES-311 — Frontend Performance Standards
- NES-208 — Redis Standards
- NES-907 — SLA & SLO Reporting

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
