---
document_id: NES-408
title: Background Sync
subtitle: Enterprise Background Tasks, TaskManager & Batch Sync Standard
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

> **"Silent background processes optimize user readiness. We execute light, power-efficient sync tasks using Expo TaskManager and BackgroundFetch."**

---

# Executive Summary

Mobile operating systems enforce strict energy budgets and background limits.

Processes that attempt to execute long-running downloads, complex calculations, or network requests in the background will be terminated by the OS, and persistent violations will cause the OS to limit the application's launch priority.

This standard defines the execution limits, scheduling options, and implementation rules for background sync using **Expo TaskManager** and **BackgroundFetch**.

---

# Purpose

This standard defines:

- Background Execution Rules (iOS/Android constraints)
- Task Registration via Expo TaskManager
- Periodic Scheduling with Expo BackgroundFetch
- Power Management and Batch Optimization
- Error Handling and OS Termination handling

---

# OS-Specific Background Constraints

We design background tasks to respect iOS and Android differences:

- **iOS (Background Fetch)**: The OS determines task execution frequency based on user usage patterns, network connectivity, and battery state. Tasks are strictly capped at **30 seconds** of execution.
- **Android (WorkManager)**: Enforces a minimum execution interval of **15 minutes** for periodic tasks. Tasks run in a native background thread.

---

# Task Manager Registration

All background tasks must be defined and registered in the global scope (outside the React component cycle), usually in `index.js` or before app mount.

- **Standard**: Use `expo-task-manager` to register named tasks.

```typescript
import * as TaskManager from 'expo-task-manager';
import * as BackgroundFetch from 'expo-background-fetch';

const BACKGROUND_SYNC_TASK = 'background-sync-task';

// Define the task
TaskManager.defineTask(BACKGROUND_SYNC_TASK, async () => {
  try {
    const hasUpdates = await performSilentSync();
    return hasUpdates 
      ? BackgroundFetch.BackgroundFetchResult.NewData 
      : BackgroundFetch.BackgroundFetchResult.NoData;
  } catch (error) {
    return BackgroundFetch.BackgroundFetchResult.Failed;
  }
});
```

---

# Task Scheduling

Schedule the registered background task contextually.

```typescript
import * as BackgroundFetch from 'expo-background-fetch';

export async function registerBackgroundFetchAsync() {
  const isRegistered = await TaskManager.isTaskRegisteredAsync(BACKGROUND_SYNC_TASK);
  if (!isRegistered) {
    throw new Error('Task must be defined in global scope first');
  }

  return BackgroundFetch.registerTaskAsync(BACKGROUND_SYNC_TASK, {
    minimumInterval: 60 * 15, // 15 minutes (minimum allowed on Android)
    stopOnTerminate: false,    // Continue running if user kills app
    startOnBoot: true,        // Restart task on device reboot
  });
}
```

---

# Power & Data Optimizations

Background processes must be designed to conserve battery and cellular data limits.

- **Check Connection**: Verify if the user is connected to Wi-Fi before initiating large file sync tasks.
- **Batch Processing**: Group multiple network updates into a single payload to minimize radio wakeups.
- **Clean Execution**: Avoid importing large UI dependencies inside background tasks. Keep task bundles focused strictly on API communication and local database write routines.

---

# Anti-Patterns

❌ **Long-running Task Requests**: Executing API calls that take more than 10-15 seconds in background fetch hooks. This leads to immediate task termination by the OS.

❌ **Dynamic State Updates inside Tasks**: Trying to update React component states (e.g. setting Zustand or React context) from a background task executing in a headless thread.

❌ **Over-scheduling Tasks**: Setting small execution intervals (e.g., trying to run tasks every 1 minute), which will be blocked or delayed by the OS system managers.

---

# Production Checklist

- [ ] Background tasks are registered at the global entry point of the app.
- [ ] Task return values correctly map to `BackgroundFetchResult` values.
- [ ] Tasks have a timeout wrapper (e.g., abort request if it takes longer than 25 seconds).
- [ ] Entitlements for background modes (fetch) are declared in `app.config.js` under the `ios` node.
- [ ] Logging is configured to output diagnostics to local databases for later crash reporting verification.

---

# Success Criteria

The Background Sync design is successful when:
- Silent updates run when the device is locked, pre-populating user caches.
- Battery usage diagnostics show the app consuming less than 2% of overall device daily consumption.
- Background tasks fail gracefully and resume on the next OS schedule slot.

---

# Document Status

**Document:** NES-408 — Background Sync
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-409 — Storage**
