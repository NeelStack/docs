---
document_id: REPO-007
title: Versioning Standard
subtitle: Semantic versioning rules for all NeelStack services, packages, and APIs
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Engineering Leadership
review_cycle: Annual
document_type: Repository Standard
parent_document: REPO-006 Code Ownership
next_document: REPO-008 Repository Governance
---

# REPO-007 — Versioning Standard

---

## Semantic Versioning

All NeelStack services, packages, and APIs use **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`):

| Part | Increment When |
|---|---|
| **MAJOR** | Breaking change (API contract broken, DB migration required) |
| **MINOR** | New feature added (backward compatible) |
| **PATCH** | Bug fix (backward compatible) |

---

## Pre-release Tags

| Tag | Meaning | Example |
|---|---|---|
| `alpha` | Internal testing only | `1.2.0-alpha.1` |
| `beta` | External preview | `1.2.0-beta.1` |
| `rc` | Release candidate | `1.2.0-rc.1` |

---

## Git Tags

Every production release MUST be tagged in Git:

```bash
git tag -a v1.2.0 -m "Release 1.2.0 — Add OAuth2 support"
git push origin v1.2.0
```

Tags trigger the CI/CD release pipeline automatically.

---

## Release Notes

Every release requires:
1. `CHANGELOG.md` updated (Keep a Changelog format)
2. GitHub Release created with release notes
3. Migration guide if MAJOR version

---

## API Versioning

See LAW-003 — API Versioning for the complete API versioning standard.

In summary:
- URL-based: `/v1/`, `/v2/`
- Breaking changes require new major version
- Old versions deprecated with 6-month notice

---

## Related Standards

- LAW-003 — API Versioning
- NES-901 — Semantic Versioning
- NES-902 — Changelogs
- REPO-008 — Repository Governance

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
