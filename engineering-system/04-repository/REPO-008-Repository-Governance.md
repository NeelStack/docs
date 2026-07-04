---
document_id: REPO-008
title: Repository Governance
subtitle: Rules and processes governing how all NeelStack repositories are managed
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Engineering Leadership
review_cycle: Annual
document_type: Repository Standard
parent_document: REPO-007 Versioning
next_document: NES-200 Python Engineering Standards
---

# REPO-008 — Repository Governance

---

## Repository Creation

New repositories require approval from Engineering Lead. Before creation:
- Define the repository's purpose in a brief RFC
- Assign CODEOWNERS
- Initialize with standard `.github/` files
- Connect to CI/CD pipeline
- Register in the Repository Registry (maintained by Platform Team)

---

## Branch Protection Rules

All `main` and `dev` branches must have these protections enabled:

| Rule | Setting |
|---|---|
| Require PR reviews | Minimum 1 reviewer |
| Dismiss stale reviews | Enabled |
| Require status checks | All CI checks must pass |
| Restrict force push | Prohibited |
| Restrict direct commits | Prohibited |
| Require signed commits | Enabled (GPG) |

---

## PR Standards

Every PR must include:
- **Title**: Follows Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`)
- **Description**: What, Why, How
- **Linked Issue**: References the GitHub Issue it resolves
- **Test evidence**: Screenshot or test output for UI/behavior changes
- **Checklist**: PR template checklist fully completed

---

## Repository Archiving

Repositories are archived (not deleted) when:
- Product is sunset
- Service is merged into another
- Prototype not progressed to production

Archived repositories are read-only with a README note explaining the archive reason and successor.

---

## Required Repository Files

Every repository must contain:

| File | Purpose |
|---|---|
| `README.md` | Project overview, setup, links |
| `CONTRIBUTING.md` | How to contribute |
| `CHANGELOG.md` | Version history |
| `LICENSE.md` | License |
| `.github/CODEOWNERS` | Ownership |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR checklist |
| `.gitignore` | Excluded files |
| `.github/workflows/ci.yml` | CI pipeline |

---

## Related Standards

- REPO-006 — Code Ownership
- NES-109 — Architecture Decision Records
- NES-1103 — Architecture Review Board

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
