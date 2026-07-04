---
document_id: NES-312
title: Frontend Testing Standards
subtitle: Enterprise Frontend Testing, Quality Assurance & Test Automation Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Frontend Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-311 Frontend Performance Standards
next_document: NES-313 Frontend Observability Standards
---

# NES-312 — Frontend Testing Standards

> **"Untested code is broken code. Every frontend component, feature, state transition, and user journey must be validated automatically to prevent regressions and secure quality."**

---

# Executive Summary

Quality is a non-negotiable attribute of every NeelStack product.

Frontend applications execute complex business logic, handle sensitive data, and host critical user journeys. 

This document defines the enterprise frontend testing standards for:

- Unit Testing
- Component Testing
- Integration Testing
- End-to-End (E2E) Testing
- Accessibility Testing
- Visual Regression Testing
- Performance and Load Testing

Our objective is to build a reliable, automated, and continuous testing pipeline that ensures product stability, prevents regressions, and maintains a high developer velocity.

---

# Purpose

This standard defines:

- Testing Architecture
- Test Levels and Coverage Targets
- Official Testing Toolchain
- Unit, Component, Integration, and E2E Standards
- Visual Regression and Accessibility Testing
- Mocking and Test Data Management
- CI/CD Quality Gates
- Code Coverage Budgets
- Testing Best Practices
- Anti-Patterns to Avoid

---

# Vision

Build a fully automated testing ecosystem capable of supporting:

- Hundreds of web and mobile applications
- Rapid release cycles (continuous deployment)
- Multi-tenant SaaS validation
- Zero-downtime releases
- Verifiable WCAG accessibility compliance

through a fast, stable, and deterministic test pipeline.

---

# Testing Philosophy

```text
Unit Tests
  (Logic)
    ↓
Component Tests
  (Isolation)
    ↓
Integration Tests
  (Data Flow)
    ↓
Visual Regression
  (Aesthetics)
    ↓
End-to-End Tests
  (Journeys)
```

No single test level can guarantee quality. We rely on a balanced testing pyramid customized for web applications.

---

# Core Principles

Every test suite must be:

✓ Deterministic (No flaky tests)

✓ Fast

✓ Isolated

✓ Maintainable

✓ Behavior-focused (Test what the user sees)

✓ Type Safe

✓ Automated

✓ Part of the CI/CD Pipeline

---

# Official Testing Toolchain

| Level | Technology | Purpose |
|---|---|---|
| Test Runner | Vitest | Fast, unit and integration runner |
| Component Testing | React Testing Library | Testing DOM in virtual browser |
| E2E Testing | Playwright | Full browser automation and visual regression |
| Mocking | MSW (Mock Service Worker) | API network-level mocking |
| Visual Regression | Playwright / Storybook | Capturing and comparing UI screenshots |
| Accessibility | axe-core | Automated WCAG compliance audits |

---

# Testing Architecture

```text
       E2E Tests (Playwright)
  ┌──────────────────────────────┐
  │   Integration (MSW + Query)  │
  ├──────────────────────────────┤
  │   Component (RTL + Vitest)   │
  ├──────────────────────────────┤
  │     Unit Tests (Vitest)      │
  └──────────────────────────────┘
```

Test logic at the lowest possible layer to keep test execution fast and diagnostic messages clear.

---

# Unit Testing Standards

Unit tests validate pure functions, utilities, and selectors.

- **Scope**: `utils/`, `helpers/`, `selectors/`, `reducers/`.
- **Target**: 100% logic coverage.
- **Rule**: Never mock internal modules; only mock external dependencies (APIs, third-party libraries).
- **Tool**: Vitest.

---

# Component Testing Standards

Component tests validate UI rendering, user interaction, and accessibility in isolation.

- **Scope**: Reusable components, primitive UI elements.
- **Rule**: Query by user-visible attributes (`role`, `name`, `text`) instead of CSS classes or test IDs.
- **Accessibility**: Run `axe` audits on every component state.
- **Tool**: React Testing Library + Vitest.

---

# Integration Testing Standards

Integration tests validate state management, data fetching, and multi-component features.

- **Scope**: Feature modules, page layouts, form submissions.
- **Rule**: Mock network requests using MSW at the request layer—never mock hooks or services directly.
- **State**: Validate that Zustand stores and TanStack Query updates trigger the correct DOM mutations.
- **Tool**: React Testing Library + MSW + Vitest.

---

# End-to-End (E2E) Testing Standards

E2E tests validate critical user journeys from login to completion against running environments.

- **Scope**: High-value flows (e.g., checkout, onboarding, document upload).
- **Rule**: Run against staging/UAT environments using headless Chrome, Firefox, and WebKit.
- **Data**: Set up and tear down test data via API calls before and after test runs.
- **Tool**: Playwright.

---

# Accessibility (a11y) Testing

All frontend components must be WCAG 2.2 AA compliant.

- **Automated**: Integrate `axe-core` in Vitest (RTL) and Playwright test suites.
- **Interactive**: Test keyboard navigation explicitly (focus state, tab order, escaping modals).
- **Verification**: Announce dynamic content to screen readers via ARIA live regions.

---

# Visual Regression Testing

Ensure changes to styles, layout, or design tokens do not cause unintended visual drift.

- **Target**: Design system, component library, dashboard layouts.
- **Execution**: Compare screenshots captured in Playwright against committed baselines.
- **Tolerance**: Zero-pixel drift allowed for core layout components.

---

# Mocking and Test Data

Mocking must be standardized to prevent divergence from backend schemas.

- **Network**: Use MSW to intercept API calls. Do not use local fetch mocks.
- **Data Generation**: Use mock factories (e.g., `@faker-js/faker`) to generate deterministic test fixtures.
- **Type Alignment**: Test fixtures must implement the exact TypeScript types generated from the OpenAPI/FastAPI schema.

---

# Continuous Integration (CI) Quality Gates

No code is merged into integration branches without passing:

```text
Code Commit
    ↓
Linter & Formatter (ESLint/Prettier)
    ↓
Type Check (tsc)
    ↓
Unit & Component Tests (Vitest)
    ↓
Accessibility Audits (axe)
    ↓
Build Verification (Next.js build)
    ↓
Visual Regression & E2E (Playwright)
```

Failed gates immediately block pull requests.

---

# Code Coverage Targets

We target quality over raw numbers, but enforce the following minimums:

| Category | Minimum Coverage |
|---|---|
| Business Logic (`utils`, `selectors`) | 90% |
| Custom Hooks (`hooks`) | 80% |
| Shared Components (`components/ui`) | 85% |
| Page / Container Components | 50% |
| Overall Project Average | 75% |

---

# Performance and Load Testing

Ensure the application remains responsive under load.

- **Core Web Vitals**: Run automated Lighthouse/Web-Vitals checks on critical routes during the CI pipeline.
- **Lighthouse Gates**:
  - Performance: >90
  - Accessibility: 100
  - Best Practices: >90
  - SEO: >90

---

# Multi-Tenancy Testing

Tests must validate tenant isolation on the client.

- Verify that switching tenants clears local/server cache.
- Confirm tenant ID is attached to all outbound headers.
- Test that tenant-specific branding (themes, logos) applies correctly.

---

# Anti-Patterns

Avoid these common testing mistakes:

- ❌ Testing internal implementation details (state, private methods).
- ❌ Hardcoding mock data directly inside test files (use shared factories instead).
- ❌ Writing flaky E2E tests that rely on arbitrary timeouts (`page.waitForTimeout`).
- ❌ Mocking API hooks instead of intercepting network requests with MSW.
- ❌ Maintaining 100% test coverage targets by writing tests that assert nothing.
- ❌ Skipping accessibility testing until manual audit phases.

---

# Production Checklist

Before deploying a frontend release:

- [ ] All Vitest unit and component tests passing.
- [ ] Playwright integration and E2E tests passing.
- [ ] Visual regression tests validated and updated.
- [ ] axe-core accessibility tests showing zero violations.
- [ ] Next.js production build passes with zero warnings.
- [ ] Code coverage targets satisfied.
- [ ] Lighthouse scores meet performance budgets.
- [ ] Verification complete.

---

# Success Criteria

The frontend testing implementation is successful when:

- Regressions are caught in the CI pipeline before reaching staging.
- Developer confidence in refactoring remains high.
- Flaky tests are eliminated (zero random failures).
- Accessible UIs are guaranteed automatically.
- Visual consistency is maintained across themes.
- Test suites run fast enough to not slow down the development lifecycle.

---

# Future Evolution

Version 2.0 will include:
- Visual regression testing portal (Storybook Chromatic equivalent)
- AI-driven automated test generation
- Flaky test detection and quarantine pipeline
- Real-time test telemetry and failure reporting
- Cross-platform test sharing (React Web + React Native Mobile)
- Architecture fitness tests for testing standards

---

# Testing Standards Checklist

- [x] Testing Architecture & Hierarchy Defined
- [x] Testing Toolchain Standardized
- [x] Unit, Component, Integration, and E2E Standards Set
- [x] Accessibility & Visual Regression Testing Included
- [x] Mocking & Test Data Management Standards Set
- [x] CI/CD Quality Gates & Coverage Targets Configured
- [x] Performance Testing Standards Included
- [x] Production Checklist & Success Criteria Set

---

# Document Status

**Document:** NES-312 — Frontend Testing Standards
**Version:** 1.0.0
**Status:** Ready for Architecture Review
**Next Document:** **NES-313 — Frontend Observability Standards**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include:
- Automated Playwright code generators
- Visual Regression platform integration guide
- AI-driven test script maintenance
- Custom testing utilities and helpers library
- Multi-browser and device matrix configurations
- Mock Service Worker (MSW) enterprise handler registry
- Continuous Performance testing integration
- C4 Testing & Automation topology diagrams
- Architecture fitness tests for code coverage compliance
