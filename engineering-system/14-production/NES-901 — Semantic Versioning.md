---
document_id: NES-901
title: Semantic Versioning
subtitle: Enterprise Semantic Versioning (SemVer) & API Compatibility Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-900 Release Management
next_document: NES-902 Changelogs
---

# NES-901 — Semantic Versioning

> **"Version numbers denote compatibility rules. We version all packages, APIs, and services using Semantic Versioning (SemVer) guidelines."**

---

# Executive Summary

In a microservice architecture, applications, libraries, and clients are highly interconnected.

If version numbers are assigned arbitrarily, developers cannot determine if updating a dependency package or calling a backend API will introduce breaking changes.

We mandate the enforcement of **Semantic Versioning (SemVer 2.0.0)** across all codebase repositories, package releases, and REST/gRPC API structures.

This standard establishes our version number formatting, API compatibility definitions, and git tagging rules.

---

# Purpose

This standard defines:

- SemVer Formatting (`MAJOR.MINOR.PATCH`)
- Increment Criteria Definitions
- API Breaking Change Boundaries
- Prerelease and Build Metadata Tags
- Git Version Tagging Rules

---

# SemVer Formatting

All version strings must follow the standard three-part format:

```text
v[MAJOR].[MINOR].[PATCH]   (e.g., v1.4.2)
```

- **MAJOR**: Incremented when you make incompatible API changes (breaking changes).
- **MINOR**: Incremented when you add functionality in a backwards-compatible manner (new features).
- **PATCH**: Incremented when you make backwards-compatible bug fixes.

---

# Increment Criteria Definitions

Apply version updates systematically based on the change scope:

### 1. PATCH Increments
- **Scope**: Internal bug fixes, security library patches, compiler version upgrades.
- **Rule**: Consumer interfaces are completely unchanged.

### 2. MINOR Increments
- **Scope**: Adding a new API endpoint, creating optional configuration variables, adding new helper utility libraries.
- **Rule**: Consumers can safely upgrade without altering their existing code.

### 3. MAJOR Increments (Breaking Changes)
- **Scope**: Renaming existing API request fields, dropping database columns, removing deprecated methods, changing authorization scopes.
- **Rule**: Consumers must refactor their applications to upgrade.

---

# Prerelease & Build Metadata

For builds compiled during active sprint testing or release candidate validation:

- **Prerelease Tags**: Append alphanumeric identifiers using a hyphen (e.g. `v1.2.0-alpha.1`, `v1.2.0-rc.3`).
- **Build Metadata**: Append build details (commit SHAs, dates) using a plus symbol (e.g., `v1.2.0-rc.3+20260704.sha83a7`).

---

# Git Version Tagging Rules

Tag releases securely in the repository logs:

- **Annotated Tags**: Enforce the use of annotated git tags (`git tag -a`) instead of lightweight tags.
- **CI Automation**: Build pipelines must parse version tags to compile deployment containers automatically:
  ```bash
  git tag -a v1.2.0 -m "Release version 1.2.0"
  git push origin v1.2.0
  ```

---

# Anti-Patterns

❌ **Static Hardcoded Version Overrides**: Keeping static version strings in configurations (e.g. `package.json` or `pyproject.toml`) that do not increment automatically during release builds.

❌ **Breaking Changes in Minor Releases**: Modifying existing database schema fields or API payload parameters inside minor or patch releases.

❌ **Excluding Git Tags**: Shipping builds to production without corresponding tags in the source code repository.

---

# Production Checklist

- [ ] Repository builds enforce SemVer increments.
- [ ] Breaking changes trigger major version bumps.
- [ ] Release branches are tagged using git annotated tag formats.
- [ ] API routes include version prefixes (e.g. `/v1/`, `/v2/`).
- [ ] Dependencies pin major versions to prevent breaks.

---

# Success Criteria

The Semantic Versioning program is successful when:
- Developers can determine if an upgrade introduces breaking changes by looking at the version string.
- API updates do not break downstream mobile or frontend clients.
- Deployment containers map directly to annotated git release tags.

---

# Document Status

**Document:** NES-901 — Semantic Versioning
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-902 — Changelogs**
