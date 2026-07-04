---
document_id: NES-800
title: QA Principles
subtitle: Enterprise Quality Assurance Principles & Shift-Left Testing Philosophy
version: 1.0.0
status: Draft
classification: Internal
owner: Quality Assurance Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-712 Reference Architecture
next_document: NES-801 Test Strategy
---

# NES-800 — QA Principles

> **"Quality is not a phase; it is a design constraint. We shift testing left to catch defects early and maintain reliability across all features."**

---

# Executive Summary

Failing to test software continuously leads to critical production bugs, emergency hotfixes, application performance drops, and customer frustration.

Relying on a late-stage manual quality assurance check right before release is slow, expensive, and fails to catch deep architectural bugs.

We mandate the integration of a **Shift-Left Quality Assurance** philosophy across all NeelStack products.

This standard outlines our QA core principles, test coverage targets, and the structural **Test Pyramid** layout.

---

# Purpose

This standard defines:

- QA Core Security and Reliability Principles
- The Shift-Left Testing Model
- The Test Pyramid Layout
- Code Coverage Target Baselines
- Continuous Verification Rules

---

# QA Core Principles

Our Quality Assurance framework is guided by three principles:

1. **Shift-Left**: Start testing activities early in the requirements and design phases—do not wait for build code completion to plan verification checks.
2. **Automate by Default**: If a test case can be executed by a script, automate it. Manual testing is reserved for exploratory reviews, visual validation, and usability checks.
3. **Prevent Defects**: Focus on preventing defects through design reviews, API typing constraints, and strict static analysis rather than just finding defects during manual validation sweeps.

---

# The Shift-Left Testing Model

Traditional testing waits for release stages, whereas our Shift-Left model validates logic during daily iteration steps:

```text
 Requirements  ──►  Design  ──►  Development  ──►  CI Build  ──►  Release
      │               │               │               │              │
  Acceptance       Threat          Unit /          E2E /          Smoke /
   Criteria       Modeling       Integration       Load           Sanity
```

---

# The Test Pyramid

To optimize verification execution speed and cost, we structure our test suites to mirror the **Test Pyramid**:

```text
              /\
             /  \     E2E UI Tests (Playwright / Detox) - Max 5%
            /----\
           /      \   Integration / API Tests - ~25%
          /--------\
         /          \ Unit Tests (Pytest / Vitest) - ~70%
        └────────────┘
```

- **Unit Tests (Base)**: High speed, low resource requirement. Validates isolated code modules. Represents the majority of tests.
- **Integration Tests (Middle)**: Verifies communication between code layers, databases, and APIs.
- **End-to-End Tests (Peak)**: Validates complete user journeys in UI layouts. Highly accurate but slow and resource-heavy. Restrict to critical paths.

---

# Code Coverage Targets

All new codebases and pull requests must meet minimum code coverage baselines:

- **Target Line Coverage**: Minimum **80%** line coverage.
- **Critical Paths (Auth, Billing, Encryption)**: Minimum **95%** coverage required.
- **CI Enforcement**: Automated gates fail PR validation runs if code modifications cause repository coverage scores to drop below active limits.

---

# Anti-Patterns

❌ **Manual Verification Gates only**: Blocking release branches manually for days to let QA engineers click through menus before shipping.

❌ **Inverted Test Pyramid (Ice Cream Cone)**: Writing few unit tests while constructing hundreds of slow, flaky E2E UI tests, leading to long build queues.

❌ **Excluding Tests from Reviews**: Approving code changes without checking if corresponding test files are included or updated.

---

# Production Checklist

- [ ] Core pipeline enforces line coverage checks.
- [ ] Staging environments use automated smoke testing scripts.
- [ ] Test pyramid ratios are verified in repositories.
- [ ] Shift-left code reviews check test designs.
- [ ] Test logs are routed to the central monitoring pipeline.

---

# Success Criteria

The QA program is successful when:
- Defects are caught in local development or CI phases, reducing production escapes.
- Build test suites execute cleanly in less than 5 minutes.
- Test coverage metrics remain stable as the codebase expands.

---

# Document Status

**Document:** NES-800 — QA Principles
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-801 — Test Strategy**
