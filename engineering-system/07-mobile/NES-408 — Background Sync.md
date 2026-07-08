---
document_id: NES-408
title: Background Sync
subtitle: Enterprise Background Tasks & Batch Sync Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Platform Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-407 Push Notifications
next_document: NES-409 Storage
---

# NES-408 — Background Sync

> **"Silent background processes optimize user readiness. We execute light, power-efficient sync tasks using Capacitor native background wrappers."**

---

# Executive Summary

Mobile operating systems enforce strict resource limits, battery budgets, and termination policies on background executions.

Processes that attempt to execute prolonged network queries or heavy computing while backgrounded will be terminated by the OS.

This standard establishes the background execution boundaries and defines how to run background synchronization in Capacitor using the **Capacitor Background Runner** (or native background task APIs).

---

# Purpose

This standard defines:

- Background Execution limits (iOS vs. Android constraints)
- Task configuration using `@capacitor/background-runner`
- Power and network optimization policies
- Error recovery and termination handles

---

# OS-Specific Background Constraints

We design background tasks to align with OS policies:

- **iOS (Background Tasks)**: The OS allocates background running slots based on battery status, network state, and usage patterns. Single runs are strictly capped at **30 seconds** of execution before termination.
- **Android (WorkManager)**: Periodic jobs require a minimum repetition interval of **15 minutes**. Tasks execute in a headless service thread.

---

# Task Configuration (Capacitor Background Runner)

We utilize `@capacitor/background-runner` to run tasks in an isolated context using Javascript/TypeScript scripts compiled natively.

- **Setup**: Define background jobs in `src/background/tasks.ts`:

```typescript
import { BackgroundRunner } from '@capacitor/background-runner';

// Register background execution task
export async function registerBackgroundSyncTask() {
  await BackgroundRunner.register({
    label: 'com.neelstack.background.sync',
    src: 'background/sync.js', // Compiled JS task script
    event: 'syncData',
    interval: 15, // Run every 15 minutes (Android min limit)
    repeats: true,
  });
}
```

- **Task Script (`sync.js`)**: Keep script files lightweight. Import only basic network clients and storage utilities:

```javascript
// background/sync.js
addEventListener('syncData', async (resolve, reject, args) => {
  try {
    // Perform light database write / fetch
    const response = await fetch('https://api.neelstack.com/sync/silent');
    const data = await response.json();
    
    // Process sync local writes...
    resolve(data);
  } catch (error) {
    reject(error);
  }
});
```

---

# Power & Network Optimization Rules

Background runner tasks must avoid draining user resources:

1. **Verify Connection**: Check if the network is on Wi-Fi before initiating large media downloads or logs uploads.
2. **Buffer and Batch**: Group multiple small requests into a single payload to minimize radio wakeups.
3. **Timeout Handlers**: Enforce a strict timeout (e.g. 25 seconds) on all network fetches inside the runner script.

```typescript
// Timeout fetch wrapper
export function fetchWithTimeout(url: string, options: RequestInit, delay = 20000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), delay);
  return fetch(url, { ...options, signal: controller.signal })
    .finally(() => clearTimeout(id));
}
```

---

# Anti-Patterns

❌ **Importing React/UI Modules in Runner Scripts**: Attempting to reference UI libraries or global stores (Zustand, React context) from a background thread. Background scripts run inside a headless worker container separate from the main web application DOM.

❌ **Forcing Short Sync Loops**: Scheduling tasks to execute every 1-2 minutes. The operating system will flag the app for CPU hogging and restrict its startup priority.

---

# Production Checklist

- [ ] Background runner scripts are packaged as standalone files in the static assets path.
- [ ] Task scripts terminate and invoke resolve/reject within the 25-second limit.
- [ ] iOS Background Modes (Background Fetch) is enabled in Xcode Capabilities.
- [ ] Diagnostic logs are written to SQLite databases to verify task completions.

---

# Success Criteria

The Background Sync implementation is successful when:
- Silent updates run when the device is locked, syncing offline queues to the cloud.
- Mobile OS battery reports show background executions consuming less than 2% of daily power.
- Task execution failures are recovered gracefully on subsequent intervals.

---

# Document Status

**Document:** NES-408 — Background Sync
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-409 — Storage**
