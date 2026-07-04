---
document_id: NES-411
title: Testing
subtitle: Enterprise Mobile Jest, React Native Testing Library & Detox Standard
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

> **"Unverified code leads to regression crashes in production. We validate our mobile code using isolated unit tests and automated E2E device simulators."**

---

# Executive Summary

Mobile releases take hours (or days) to pass app store reviews.

Fixing a critical crash in production is a slow process compared to web hotfixes.

Thus, rigorous automated testing is mandatory for mobile.

This standard defines our mobile testing pyramid, toolchains, coverage metrics, and integration tests using **Jest**, **React Native Testing Library**, and **Detox**.

---

# Purpose

This standard defines:

- Unit and Integration Testing (Jest + RNTL)
- Network mocking (Mock Service Worker / MSW)
- End-to-End Testing (Detox)
- Automated Test runs on CI/CD pipelines
- Code Coverage Budgets

---

# Testing Toolchain

We standardize on the following testing toolchain:

| Level | Tool | Focus |
|---|---|---|
| Test Runner | Jest | Fast, snapshot, and assertion runner |
| Component UI | React Native Testing Library (RNTL) | Virtual DOM interaction and accessibility checks |
| Mocking | Mock Service Worker (MSW) | Network-level API mocking |
| E2E Testing | Detox | Full-device simulation (Grey-box automated testing) |

---

# Unit & Component Testing (Jest + RNTL)

Unit tests validate business utilities, hooks, state transitions, and UI components in isolation.

- **Query by Text/Role**: Avoid querying by test IDs or styles. Test what the user sees or interacts with.
- **Act Block**: Always wrap state-modifying actions inside the `act` function to ensure consistent DOM states.

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Button } from './Button';

test('renders button label and fires onPress callback', () => {
  const mockPress = jest.fn();
  render(<Button label="Submit" onPress={mockPress} />);

  const buttonElement = screen.getByText('Submit');
  fireEvent.press(buttonElement);

  expect(mockPress).toHaveBeenCalledTimes(1);
});
```

---

# Network Mocking (MSW)

Do not mock network hooks or global fetch functions inside tests. This leads to brittle tests that break on refactoring.

- **Standard**: Intercept API requests at the network layer using **Mock Service Worker (MSW)**.
- **Benefit**: Ensures tests validate the real data exchange format and catch serialization bugs.

```typescript
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.get('https://api.neelstack.com/documents', () => {
    return HttpResponse.json([{ id: '1', title: 'Test Certificate' }]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---

# End-to-End (E2E) Testing (Detox)

We use **Detox** to run E2E grey-box testing inside actual iOS simulators and Android emulators.

- **Grey-box Execution**: Detox monitors app activity (network requests, layout cycles, animations) to avoid flaky checks and synchronize test actions with app idle state.
- **Rule**: Run E2E tests against local test server configurations to protect production environments from test data pollution.

```typescript
describe('Authentication Flow', () => {
  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should navigate to login page and login successfully', async () => {
    await expect(element(by.text('Welcome'))).toBeVisible();
    
    // Type in credentials
    await element(by.id('email-input')).typeText('student@neelstack.edu');
    await element(by.id('password-input')).typeText('SecurePassword123');
    await element(by.text('Login')).tap();

    // Verify main screen navigation
    await expect(element(by.text('Dashboard'))).toBeVisible();
  });
});
```

---

# CI/CD Quality Gates

All pull requests targeting production or integration branches must pass through automated test suites.

```text
Pull Request Submitted
          │
    ESLint & Typecheck
          │
  Unit Tests (Jest)
          │
   Coverage Checked
          │
 Detox E2E (Simulators)
          │
    Merge Approved
```

---

# Code Coverage Targets

Mobile code coverage targets ensure core business flow validation:

- **Business Logic (`utils`, `helpers`)**: Min 90%
- **State stores (`Zustand`)**: Min 80%
- **Forms & Inputs validation**: Min 90%
- **UI Components**: Min 60%

---

# Anti-Patterns

❌ **Relying Solely on Test IDs**: Querying components like `element(by.id('my-input'))` everywhere. Querying by accessibility labels or text strings makes tests screen-reader friendly and aligns with user experience.

❌ **Hardcoded Wait Times**: Writing E2E steps with raw timers like `await new Promise(r => setTimeout(r, 5000))`. This slows down builds and causes flakiness on slower CI hardware. Rely on automated synchronization.

❌ **Mocking the React Native Core**: Mocking imports like `Platform` or core layout modules inside Jest, which masks layout bugs.

---

# Production Checklist

- [ ] Jest configuration runs with Hermes Babel transformer.
- [ ] All MSW handlers align with backend FastAPI API schemas.
- [ ] Detox config runs on headless emulator engines in CI/CD pipeline.
- [ ] Code coverage thresholds are configured as block-gates in the pipeline.
- [ ] Unit and component test suites run in less than 3 minutes.

---

# Success Criteria

The Testing standards are successful when:
- Zero regressions reach the app store releases.
- E2E tests pass on CI pipelines without flaky failures.
- Developers can write and verify local tests in their workspaces with rapid feedback.

---

# Document Status

**Document:** NES-411 — Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-412 — Release**
