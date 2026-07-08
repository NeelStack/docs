---
document_id: NES-414
title: Crash Reporting
subtitle: Enterprise Mobile Crash Reporting, Sentry & Error Boundary Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-413 Analytics
next_document: NES-415 Mobile AI
---

# NES-414 — Crash Reporting

> **"Unreported crashes are unresolved bugs. We capture uncaught JavaScript exceptions, native crashes, and configure automated alert reporting."**

---

# Executive Summary

Mobile applications can fail due to JavaScript runtime errors, native platform out-of-memory states, or container Webview issues.

We automate exception capturing at both the JavaScript web bundle layer and native layers (Objective-C/Swift and Java/Kotlin) using **Sentry for Capacitor**.

---

# Purpose

This standard defines:

- Sentry configuration rules under Capacitor
- React Error Boundary setup (Web/DOM elements)
- Automated Sourcemaps upload using the Vite Sentry plugin
- Operational alert SLAs

---

# Tooling Standard (Sentry for Capacitor)

We standardize on **`@sentry/capacitor`** for all mobile platforms.

- **Initialization**: Initialize the Sentry SDK inside the web application boot module (`main.tsx`):

```typescript
import * as Sentry from '@sentry/capacitor';

Sentry.init({
  dsn: 'https://xxxxxxxx@sentry.io/xxxxxx',
  release: 'neelstack-portal-mobile@1.0.0',
  dist: '1',
  tracesSampleRate: 0.1,
});
```

---

# React Error Boundaries

We wrap root layout routes inside a React Error Boundary to capture rendering failures and show recovery layouts rather than letting the application crash back to the device dashboard.

- **Component Example**:

```tsx
import * as Sentry from '@sentry/capacitor';
import React from 'react';

interface Props {
  children: React.ReactNode;
}

export function ErrorBoundaryFallback({ error, resetError }: { error: Error; resetError: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-slate-50 text-center">
      <h2 className="text-xl font-bold text-slate-900">Something went wrong</h2>
      <p className="mt-2 text-sm text-slate-500 max-w-sm">{error.message}</p>
      <button
        onClick={resetError}
        className="mt-6 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
      >
        Reload Page
      </button>
    </div>
  );
}

export function GlobalErrorBoundary({ children }: Props) {
  return (
    <Sentry.ErrorBoundary fallback={(props) => <ErrorBoundaryFallback {...props} />}>
      {children}
    </Sentry.ErrorBoundary>
  );
}
```

---

# Sourcemaps Upload Automation

JavaScript code is compiled and obfuscated in production. Sentry crash traces from these bundles are unreadable without map files.

- **Vite Integration**: We use **`@sentry/vite-plugin`** inside `vite.config.ts` to build and upload sourcemaps automatically to the Sentry server during `npm run build`:

```typescript
import { defineConfig } from 'vite';
import { sentryVitePlugin } from '@sentry/vite-plugin';

export default defineConfig({
  plugins: [
    sentryVitePlugin({
      org: 'neelstack',
      project: 'portal-mobile',
      authToken: process.env.SENTRY_AUTH_TOKEN,
    }),
  ],
  build: {
    sourcemap: true, // Required for Sentry uploads
  }
});
```

- **Security**: Never commit `SENTRY_AUTH_TOKEN` inside the repository. Inject it via GitHub Actions CI pipeline secrets.

---

# Anti-Patterns

❌ **Catching Errors Silently**: Swallowing exceptions inside `try/catch` scopes without forwarding them to Sentry:
   ```typescript
   try {
     // API fetch
   } catch (error) {
     console.log(error); // AVOID
   }
   ```
   Always capture log markers for diagnostic tracking:
   ```typescript
   Sentry.captureException(error);
   ```

❌ **Manual Sourcemap Uploads**: Requiring developers to zip and upload map outputs manually, leading to broken stack traces.

---

# Production Checklist

- [ ] Sentry DSN configuration is injected via environment variables.
- [ ] Root routing is wrapped inside the Global Error Boundary component.
- [ ] Sourcemaps are verified as uploaded during the CI compilation stage.
- [ ] Slack/Teams integrations are configured to track critical errors.

---

# Success Criteria

The Crash Reporting implementation is successful when:
- WebView exceptions generate readable traces pointing to active TypeScript filenames and line numbers.
- Crashes log user action sequences (e.g. navigation clicks, event pushes) leading to the error.
- Alerts dispatch immediately on production crash events.

---

# Document Status

**Document:** NES-414 — Crash Reporting
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-415 — Mobile AI**
