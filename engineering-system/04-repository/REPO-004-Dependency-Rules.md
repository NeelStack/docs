---
document_id: REPO-004
title: Dependency Rules
subtitle: Rules for adding, upgrading, and auditing dependencies across all NeelStack repositories
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Repository Standard
parent_document: REPO-003 Package Structure
next_document: REPO-005 Import Rules
---

# REPO-004 — Dependency Rules

---

## Adding a New Dependency

Before adding any new dependency, evaluate:

1. **Is it necessary?** Can the functionality be implemented in < 50 lines without a library?
2. **Is it maintained?** Last commit within 6 months, active maintainers.
3. **Is it secure?** No known CVEs in the latest version.
4. **Is the license compatible?** MIT, Apache 2.0, BSD preferred. GPL requires legal review.
5. **What is the bundle impact?** For frontend packages: check bundle size impact.

New dependencies added to shared packages require **ARB approval**.

## Approved Dependency Audit Tools

| Platform | Tool | Frequency |
|---|---|---|
| Python | `pip-audit` | Every PR |
| Node.js | `npm audit` | Every PR |
| Container | `trivy` | Every build |
| SBOM | `syft` | Every release |

## Dependency Update Policy

- **Security patches**: Apply within 24 hours of disclosure
- **Minor updates**: Apply monthly via automated PRs (Renovate/Dependabot)
- **Major updates**: Apply after testing, require changelog review
- Never upgrade a major version in a hotfix

## Prohibited Packages

The following packages are prohibited without explicit security review:

| Package | Reason |
|---|---|
| `eval()`, `exec()` (Python) | Code injection risk |
| `jsonpickle` | Deserialization attacks |
| `pickle` (in API paths) | Deserialization attacks |
| `lodash` < 4.17.21 | Known vulnerabilities |
| `moment.js` | Use `date-fns` or `dayjs` instead |

## SBOM (Software Bill of Materials)

Every release generates an SBOM documenting all direct and transitive dependencies. SBOM stored in S3 with release artifacts.

## Related Standards

- LAW-007 — Security
- NES-608 — Supply Chain Security
- REPO-003 — Package Structure

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
