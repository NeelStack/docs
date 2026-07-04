---
document_id: NES-405
title: Offline Architecture
subtitle: Enterprise Mobile Offline-First, Connectivity & Conflict Resolution Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-404 State
next_document: NES-406 Mobile Security
---

# NES-405 — Offline Architecture

> **"Mobile networks are inherently unstable. Our applications must work seamlessly offline and synchronize data intelligently when connectivity is restored."**

---

# Executive Summary

Users expect enterprise mobile applications to remain functional in areas with poor or absent network connectivity (e.g. basements, rural fields, elevators, transport systems).

An application that crashes or locks up when offline is unacceptable.

This standard defines the architecture for local caching, mutation queueing, background synchronization, and sync conflict resolution.

---

# Purpose

This standard defines:

- Offline-First Design patterns
- Connectivity detection using NetInfo
- Local request queueing
- Data synchronization pipelines
- Conflict resolution strategies (Last-Write-Wins, Client-First, Merge)

---

# Connectivity Detection (NetInfo)

All mobile apps must monitor network state globally.

- **Library**: Use `@react-native-community/netinfo`.
- **Global Context**: Expose network state via a provider or hook so UI components can display warning banners or disable online-only features dynamically.

```typescript
import NetInfo from '@react-native-community/netinfo';
import { create } from 'zustand';

interface NetworkState {
  isConnected: boolean;
  isInternetReachable: boolean;
  setConnection: (connected: boolean, reachable: boolean) => void;
}

export const useNetworkStore = create<NetworkState>((set) => ({
  isConnected: true,
  isInternetReachable: true,
  setConnection: (connected, reachable) => set({
    isConnected: connected,
    isInternetReachable: reachable
  }),
}));

// Initialize in root layout
NetInfo.addEventListener((state) => {
  useNetworkStore.getState().setConnection(
    state.isConnected ?? false,
    state.isInternetReachable ?? false
  );
});
```

---

# Mutation Queueing (Offline Write)

When a user performs an action (e.g. updates a form or submits a record) while offline, we do not throw an error. Instead, we queue the transaction locally.

- **Persistent Queue**: Write mutation payloads (endpoint, method, request body, timestamp) to local storage (SQLite or AsyncStorage).
- **Retry Daemon**: When network connectivity is restored, trigger a sync task to drain the queue sequentially.

```typescript
interface OfflineMutation {
  id: string;
  url: string;
  method: 'POST' | 'PUT' | 'DELETE';
  body: string; // JSON payload
  timestamp: number;
}

export async function queueMutation(mutation: Omit<OfflineMutation, 'id' | 'timestamp'>) {
  const newMutation: OfflineMutation = {
    ...mutation,
    id: uuid.v4() as string,
    timestamp: Date.now(),
  };
  
  // Read existing queue
  const currentQueue = await getOfflineQueue();
  currentQueue.push(newMutation);
  
  // Save to persistent storage
  await saveOfflineQueue(currentQueue);
}
```

---

# Conflict Resolution

When synchronizing cached modifications, conflicts with the server's state will occur. We define three resolution policies:

### 1. Last-Write-Wins (LWW)
- **Policy**: The client update overwrites the server update if its timestamp is newer.
- **Requirement**: Client and server clocks must be synchronized via NTP check offset.

### 2. Client-First / Server-First
- **Policy**: Explicitly prioritize either the mobile device state or the cloud database state.

### 3. User Resolution / Interstitial Merge
- **Policy**: Prompt the user with a diff layout showing the server modifications and their local modifications, allowing them to choose which to save.

```text
       Sync Mutation Sent
               │
      ┌────────┴────────┐
      ▼                 ▼
No Conflict      Conflict Detected
      │                 │
Apply Change      Apply Resolution Policy:
                  ├── Last-Write-Wins
                  ├── Client-First
                  └── User Merge Selection
```

---

# Client Data Prefetching

Optimize the offline experience by proactively caching pages/records.

- **Prefetch Hook**: Pre-populate TanStack query cache for details views before the user taps on them (e.g., prefetch list items on list view rendering).
- **Asset Caching**: Configure `expo-image` to aggressive-cache images locally.

---

# Anti-Patterns

❌ **Blocking UI with Spinners**: Displaying block screens during sync tasks. Operations should occur in the background, showing status badges instead.

❌ **Unlimited Retry Loops**: Attempting to send requests repeatedly without backing off, which drains mobile battery and overloads backend servers.

❌ **Not Syncing in Order**: Draining the mutation queue out of order (e.g. attempting to update a resource before sending the creation request).

---

# Production Checklist

- [ ] NetInfo listener is initialized correctly at the app entry point.
- [ ] Offline queue is stored securely and survives app reboots.
- [ ] Clear visual indicator (e.g., a "Syncing..." or "Offline Mode" icon) is present in the UI.
- [ ] Back-off strategy (exponential back-off) is implemented for sync retry loops.
- [ ] Conflict resolution tests have been run.

---

# Success Criteria

The Offline design is successful when:
- Users can create and edit resources completely offline without UI interruption.
- The app automatically syncs queued modifications immediately when network connectivity is restored.
- Conflicts are handled cleanly without crashing the client or corrupting the backend database.

---

# Document Status

**Document:** NES-405 — Offline Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-406 — Mobile Security**
