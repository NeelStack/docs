---
document_id: NES-411
title: Testing
subtitle: Enterprise Vitest, React Testing Library & Playwright/Appium Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-410 Mobile Performance
next_document: NES-412 Release
---

# NES-411 — Testing

> **"Unverified code leads to regression crashes in production. We validate our hybrid mobile code using Vitest and verify E2E integration inside WebView containers."**

---

# Executive Summary

Mobile releases require hours (or days) to pass through app store reviews. Hotfixing critical errors is significantly slower than on web platforms.

We enforce a strict testing hierarchy. We use **Vitest** + **React Testing Library** for fast, local component and logic tests, and **Playwright** (or Appium) for automated integration testing.

---

# Purpose

This standard defines:

- Unit and component testing configurations (Vitest + React Testing Library)
- Network request mocking using MSW
- End-to-End container testing (Playwright / Appium)
- CI/CD quality gate rules

---

# Testing Toolchain

| Level | Tool | Focus |
|---|---|---|
| Test Runner | **Vitest** | Fast, Vite-compatible JS unit and utility runner |
| Component UI | **React Testing Library** | DOM interaction and access checks |
| Mocking | **Mock Service Worker (MSW)** | Network-level API interceptor |
| E2E Testing | **Playwright / Appium** | Full container-level simulation |

---

# Unit & Component Testing (Vitest + RTL)

Unit tests validate business utilities, hooks, stores, and React components.

- **Query Principles**: Avoid selecting elements by internal styles or test IDs. Query by role, text, or accessibility tags.
- **Act Blocks**: Ensure async state updates are wrapped in `act()` checks.

```typescript
import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button Component', () => {
  test('renders button text and triggers click event', () => {
    const handlePress = vi.fn();
    render(<Button label="Submit" onClick={handlePress} />);

    const button = screen.getByRole('button', { name: 'Submit' });
    fireEvent.click(button);

    expect(handlePress).toHaveBeenCalledTimes(1);
  });
});
```

---

# Network Mocking (MSW)

We intercept network endpoints at the protocol layer using MSW instead of manually stubbing axios/fetch.

```typescript
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { beforeAll, afterEach, afterAll } from 'vitest';

const server = setupServer(
  http.get('https://api.neelstack.com/documents', () => {
    return HttpResponse.json([{ id: '1', title: 'Standard Certificate' }]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---

# End-to-End (E2E) Testing (Playwright / Appium)

We verify the combined native and web features in one pipeline:

- **Playwright (Web layer)**: Inspects the Vite web application directly under simulated device viewports, verifying all routing and layouts.
- **Appium (Container layer)**: Runs automation scripts inside iOS/Android emulators, targeting the WKWebView/Chromium wrapper for true native-to-bridge validation.

```typescript
// Playwright Web integration test example
import { test, expect } from '@playwright/test';

test.describe('Mobile Portal Authentication', () => {
  test('should log in and display dashboard', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    
    await page.getByLabel('Email').fill('student@neelstack.edu');
    await page.getByLabel('Password').fill('SecurePassword123');
    await page.click('button:has-text("Login")');

    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  });
});
```

---

# CI/CD Quality Gates

```text
  Pull Request Opened
          │
          ▼
  Vitest Runner Checks (Units & Hooks)
          │
          ▼
  Linter and TypeScript Compile Pass
          │
          ▼
  Playwright E2E Integration Run
          │
          ▼
  Merge to Main Approved
```

---

# Anti-Patterns

❌ **Hardcoded UI Sleep Statements**: Writing tests with static wait times (`await new Promise(r => setTimeout(r, 5000))`), which slows down CI pipelines. Use RTL's `waitFor` or Playwright auto-waiting methods.

❌ **Mocking the DOM Engine**: Stubbing window navigation features manually in Vitest instead of verifying them inside the virtual router container.

---

# Production Checklist

- [ ] Vitest configs match Vite module aliases configuration.
- [ ] MSW intercept handlers validate response structures.
- [ ] Playwright web integration runs pass before release pushes.
- [ ] Code coverage reports verify 80% coverage on core stores/helpers.

---

# Success Criteria

The Testing standards are successful when:
- Zero critical layout regressions bypass testing to reach app store releases.
- Unit and logic test suites execute under 1 minute.
- E2E scripts run stably without intermittent flakiness.

---

# Document Status

**Document:** NES-411 — Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-412 — Release**
