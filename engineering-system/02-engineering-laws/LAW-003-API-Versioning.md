---
document_id: LAW-003
title: API Versioning
subtitle: All public APIs must be versioned from day one — breaking changes require a new version
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Chief Architect
review_cycle: Annual
document_type: Engineering Law
parent_document: LAW-002 Domain Ownership
next_document: LAW-004 Observability
---

# LAW-003 — API Versioning

> **"An API without a version is a promise you cannot keep. Every external contract must be versioned before the first consumer exists."**

---

## Law Statement

**Every API endpoint that is consumed by an external system, another service, or any client MUST carry an explicit version identifier. Breaking changes MUST be introduced in a new version. Old versions MUST be deprecated with a minimum 6-month notice.**

---

## Versioning Standard

All NeelStack APIs use **URL-based versioning**:

```
https://api.neelstack.com/v1/users
https://api.neelstack.com/v2/users
```

### Version Lifecycle

| Stage | Duration | Action |
|---|---|---|
| **Active** | Indefinite | Fully supported, SLA applies |
| **Deprecated** | Minimum 6 months | Supported with deprecation header |
| **Sunset** | After deprecation period | Returns `410 Gone` |

---

## Breaking vs Non-Breaking Changes

### Non-Breaking (allowed in existing version)
- Adding new optional fields to response
- Adding new optional query parameters
- Adding new endpoints
- Reducing response latency

### Breaking (requires new version)
- Removing a field from response
- Renaming a field
- Changing a field's data type
- Making an optional field required
- Changing authentication scheme
- Changing URL path structure

---

## Deprecation Headers

When a version is deprecated, every response MUST include:

```http
Deprecation: true
Sunset: Sat, 04 Jul 2026 00:00:00 GMT
Link: <https://api.neelstack.com/v2/users>; rel="successor-version"
```

---

## Internal Service APIs

Internal service-to-service APIs follow the same rule. No internal API is exempt. Services that ignore versioning create tight coupling that breaks on every deploy.

---

## Anti-Patterns

❌ `/api/users` — No version, breaking changes will break all consumers immediately.  
❌ Versioning via `?version=2` query param — Not a standard, hard to route.  
❌ Releasing breaking changes in the same version with "migration guides."

---

## Related Standards

- NES-202 — API Design Standards
- NES-108 — Service Communication
- LAW-002 — Domain Ownership

---

## Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0.0 | 2026-07-04 | NeelStack Engineering | Initial publication |
