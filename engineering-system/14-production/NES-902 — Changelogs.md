---
document_id: NES-902
title: Changelogs
subtitle: Enterprise Keep a Changelog & Conventional Commit Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-901 Semantic Versioning
next_document: NES-903 Feature Flags
---

# NES-902 — Changelogs

> **"Changes must be documented and searchable. We automate changelog compilation using Conventional Commits and Keep a Changelog layouts."**

---

# Executive Summary

When updating platforms, product managers, support teams, and external clients require clear release summaries detailing additions, fixes, and deprecations.

If developers construct logs manually or generate raw git commit logs containing unstructured messages (e.g. "fix bug"), changelogs become unreadable.

We mandate the adoption of the **Keep a Changelog** standard.

This standard establishes our log categorization guidelines, conventional commit rules, and automated release notes generation pipelines.

---

# Purpose

This standard defines:

- Keep a Changelog Format Conventions
- Conventional Commits Enforcements
- Automated Changelog Generation (CI)
- Log Categories (Added, Changed, Fixed, Security)
- Release Communication Targets

---

# Keep a Changelog Format

Every codebase repository must maintain a `CHANGELOG.md` file in its root directory following the standard markdown layout:

- **Group Changes**: Group modifications by category (Added, Changed, Deprecated, Removed, Fixed, Security).
- **Descending Order**: Place new releases at the top, listing the release date and a link to the git tag difference.

### Reference Changelog Markdown Structure:

```markdown
# Changelog
All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-07-04
### Added
- Integrated dynamic PDF export for school certificates (NES-409).
- Added multi-factor authentication (MFA) enforcement policies in Entra ID sync.

### Fixed
- Fixed memory leakage in PDF compilation worker loops (INCIDENT-FIX-987).

### Security
- Upgraded node base image to v22-alpine to patch CVE-2026-12345.
```

---

# Conventional Commits Enforcement

To automate changelog generation, developers must write commit messages conforming to the **Conventional Commits** specification:

- **Format**:
  ```text
  <type>(<scope>): <description>

  [optional body]

  [optional footer(s)]
  ```
- **Approved Types**:
  - `feat`: A new user-facing feature (maps to **Added** in changelog).
  - `fix`: A bug fix (maps to **Fixed** in changelog).
  - `docs`: Documentation changes.
  - `style`: Code formatting updates (whitespace, formatting).
  - `refactor`: Code changes that neither fix a bug nor add a feature.
  - `chore`: Upgrading dependencies, build scripts, or CI/CD tasks.

- **Breaking Changes**: Declare breaking changes by appending an exclamation mark after the type (e.g. `feat!:` or `refactor!:`) and detailing the change in the footer.

---

# Automated Changelog Generation

We automate changelog updates inside build pipelines:

- **Semantic Release**: Use tools like `semantic-release` or `auto-changelog` to parse commit logs since the last tag.
- **Auto Commit**: The pipeline compiles release summaries, commits updates to `CHANGELOG.md`, increments the version number, and tags the git commit hash automatically.

---

# Anti-Patterns

❌ **Manual Git Commit Dumps**: Generating release notes by outputting raw, un-filtered git commit lines (e.g., `git log`) directly to clients.

❌ **Vague Commit Titles**: Committing changes with titles like `temp fix` or `updates`. Commit linting hooks must reject these.

❌ **Exposing Internal Issues**: Including developers' names, sensitive server paths, or internal Jira discussions in public release logs.

---

# Production Checklist

- [ ] `CHANGELOG.md` is initialized in the repository root.
- [ ] Commit linting hooks (husky + commitlint) block invalid commits locally.
- [ ] Conventional commit rules are active for pull request merges.
- [ ] Automated changelog generation script is configured in CI.
- [ ] Release notes generation maps to target categories.

---

# Success Criteria

The Changelog program is successful when:
- Release logs compile automatically on every version increment without manual editing.
- Client teams can search and identify feature additions by date.
- Commit logs conform to a single, easily parseable design structure.

---

# Document Status

**Document:** NES-902 — Changelogs
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-903 — Feature Flags**
