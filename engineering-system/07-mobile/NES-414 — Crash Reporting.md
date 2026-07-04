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

> **"Unreported crashes are unresolved bugs. We capture uncaught exceptions, upload sourcemaps automatically, and configure proactive error alerts."**

---

# Executive Summary

Mobile applications can fail due to unhandled JavaScript exceptions, native thread memory out-of-bounds, library memory leaks, or network timeouts.

When a crash occurs on a customer's device, we cannot rely on manual bug reports. We must collect diagnostic reports automatically.

This standard defines the crash logging architecture, error boundary configurations, sourcemap upload automation, and alert rules using **Sentry**.

---

# Purpose

This standard defines:

- Crash reporting platform selection (Sentry)
- React Error Boundary configurations
- Global Exception Handlers (JS and Native threads)
- Sourcemap generation and automated uploads
- Alerting thresholds and operational response SLA

---

# Tooling Standard (Sentry)

We standardize on **Sentry** for mobile error monitoring, tracing, and exception reporting.

- **Unified SDK**: Integrate `sentry-expo` or `@sentry/react-native` to capture errors on both JS and native levels (Objective-C/Swift, Java/Kotlin).
- **Environment Separation**: Configure Sentry tags for environment tagging (`development`, `staging`, `production`) and release versions.

---

# Global Error Boundaries

Implement a top-level React Error Boundary to catch UI-level rendering exceptions and display a fallback screen rather than letting the application crash to the device home screen.

- **Standard**: Wrap the root layout in `Sentry.ErrorBoundary` or a custom component.
- **Behavior**: Display a friendly recovery screen that allows the user to reload the app or contact support.

```typescript
import * as Sentry from '@sentry/react-native';
import { View, Text, Button } from 'react-native';

function FallbackComponent({ error, resetError }: { error: Error; resetError: () => void }) {
  return (
    <View className="flex-1 items-center justify-center p-6 bg-slate-50">
      <Text className="text-xl font-bold text-slate-900">Something went wrong</Text>
      <Text className="mt-2 text-sm text-slate-500 text-center">{error.message}</Text>
      <View className="mt-6 w-full max-w-xs">
        <Button title="Reload App" onPress={resetError} />
      </View>
    </View>
  );
}

export default Sentry.wrap(function AppLayout() {
  return (
    <Sentry.ErrorBoundary fallback={FallbackComponent}>
      <Stack />
    </Sentry.ErrorBoundary>
  );
});
```

---

# JS & Native Exception Handlers

Exceptions can occur outside the React render lifecycle (e.g. background sync threads, promise rejections, native components).

- **Unhandled Promise Rejections**: Configure Sentry to intercept and log unhandled rejections automatically.
- **Native Crash Handlers**: Ensure Sentry's native hooks are initialized in `app.json` via config plugins to capture out-of-memory (OOM) failures or JVM crashes.

```json
{
  "expo": {
    "plugins": [
      [
        "@sentry/react-native/expo",
        {
          "organization": "neelstack",
          "project": "portal-mobile"
        }
      ]
    ]
  }
}
```

---

# Sourcemaps Upload Automation

JavaScript code is minified and obfuscated in production builds. Raw crash stacks from these builds are unreadable.

- **Standard**: Generate and upload JavaScript **Sourcemaps** to Sentry during EAS Build runs.
- **Automation**: Configure EAS hooks to run Sentry sourcemap upload commands automatically:

```json
{
  "hooks": {
    "postPublish": [
      {
        "file": "sentry-expo/upload-sourcemaps",
        "config": {
          "organization": "neelstack",
          "project": "portal-mobile"
        }
      }
    ]
  }
}
```

Never commit Sentry auth tokens to public code repos. Inject them via EAS environment variables.

---

# Anti-Patterns

❌ **Catching and Swallowing Exceptions**: Writing try-catch blocks that suppress errors without forwarding them to Sentry:
   ```typescript
   try { ... } catch(e) { console.log(e); } // WRONG: Swallows error
   ```
   If an exception occurs that breaks the user flow, log it explicitly:
   ```typescript
   Sentry.captureException(e);
   ```

❌ **Uploading Sourcemaps Manually**: Relying on developers to upload sourcemaps from their local machines post-release. This leads to missing sourcemaps and unreadable logs.

❌ **Exposing Credentials in Stack Traces**: Allowing secure passwords, authentication keys, or PII to be logged inside error payloads. Filter out sensitive values using Sentry's `beforeSend` interceptor.

---

# Production Checklist

- [ ] Sentry DSN is configured via environment variables.
- [ ] Root layout is wrapped in the Sentry Error Boundary.
- [ ] Sourcemap uploads are verified on release build compilations.
- [ ] Native exception handler plugins are declared.
- [ ] Team alert integrations (e.g., Slack, PagerDuty) are active for production crash spikes.

---

# Success Criteria

The Crash Reporting setup is successful when:
- Unhandled crashes generate readable, de-minified stack traces pointing directly to file names and line numbers.
- Crash events display breadcrumbs detailing user steps (navigation path, button clicks) leading to the exception.
- Production crashes generate instant alerts for the mobile operations on-call team.

---

# Document Status

**Document:** NES-414 — Crash Reporting
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-415 — Mobile AI**
