---
document_id: NES-804
title: E2E Testing
subtitle: Enterprise End-to-End Web & Mobile UI Testing Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Quality Assurance Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-803 Integration Testing
next_document: NES-805 Performance Testing
---

# NES-804 — E2E Testing

> **"E2E tests validate complete user journeys. We write stable, flaky-resistant UI tests using Playwright and Detox, targeting critical paths."**

---

# Executive Summary

End-to-End (E2E) testing mimics real user interactions by loading web applications in browsers or mobile apps on simulators to verify workflows (e.g. login, invoice payment, document compilation).

If E2E tests are poorly designed, they experience high flakiness (tests failing due to network timing or slow renders rather than real bugs) and block release pipelines.

This standard establishes our E2E testing guidelines, approved frameworks, selector rules, and flakiness mitigation strategies.

---

# Purpose

This standard defines:

- Standardized E2E Frameworks (Playwright, Detox)
- Critical Paths Definition (The Smoke Core)
- Selector Standards (Data Attributes)
- Test State Setup and Cleanup
- Flakiness Mitigation Strategies

---

# Approved E2E Testing Tooling

We restrict E2E automation to two frameworks:

- **Web Applications**: **Playwright** (running tests in parallel across headless Chromium, Firefox, and WebKit).
- **Mobile Applications**: **Detox** (executing grey-box UI automation on iOS Simulator and Android Emulator instances).

---

# Selector Standards (Targeting UI Elements)

Prohibit the targeting of UI components using unstable criteria like CSS classes, layout paths (XPath), or raw button text strings, which change frequently during design updates.

- **Standard**: Always target components using dedicated, immutable test data attributes:
  - **Web**: `data-testid="button-submit-invoice"`
  - **Mobile**: `testID="button-submit-invoice"`
- **Benefits**: Decouples UI testing assertions from design styles, colors, and translations.

```tsx
// Correct React Native target styling
<TouchableOpacity 
  testID="button-submit-invoice"
  onPress={handleSubmit}
>
  <Text>Submit Invoice</Text>
</TouchableOpacity>
```

---

# Test State Setup & Isolation

E2E tests must be self-contained:

- **No Shared State**: Tests must not rely on previous steps or other tests.
- **Automated Setup**: Populate necessary database states prior to test runs via API calls rather than driving the UI to set up test scenarios.
- **Teardown**: Delete test files and data records via database commands post-execution to prevent test data leakage.

---

# Flakiness Mitigation Strategies

To maintain a reliable testing pipeline:

- **Auto-Wait**: Do not use hardcoded timeouts (e.g. `await page.waitForTimeout(5000)`). Use Playwright/Detox built-in auto-waiting mechanisms which check if components are visible, active, and stable before attempting actions.
- **Automatic Retries**: Configure runners to automatically retry failed tests a maximum of **2 times** in CI pipelines before declaring a test failure.

---

# Anti-Patterns

❌ **Hardcoded UI Sleep Loops**: Inserting static wait loops (`sleep(5)`) inside test steps to wait for database updates or page loads.

❌ **Exposing Production Accounts**: Running automated E2E tests against live production servers using hardcoded admin credentials.

❌ **Automating All UI Flows**: Writing E2E tests for every button layout combination. This leads to slow execution times. Validate minor UI flows via unit or component tests instead.

---

# Production Checklist

- [ ] Web E2E tests utilize Playwright.
- [ ] Mobile tests are automated using Detox.
- [ ] Element selectors use `data-testid` or `testID` conventions.
- [ ] Hardcoded timeouts (`sleep`) are removed from tests.
- [ ] Test states are isolated and clean up post-run.

---

# Success Criteria

The E2E Testing program is successful when:
- Critical path smoke runs execute cleanly in CI on every release branch.
- Flakiness rates (tests failing due to timing issues rather than bugs) remain below 1%.
- Automated test runs isolate and identify broken UI states before release deployment.

---

# Document Status

**Document:** NES-804 — E2E Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-805 — Performance Testing**
