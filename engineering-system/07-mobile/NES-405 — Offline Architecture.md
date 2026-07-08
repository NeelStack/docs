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

Enterprise mobile applications must remain functional in zones with poor or absent network connectivity (e.g., basements, elevators, transit tunnels, remote areas).

We implement an **Offline-First** model where read datasets are cached locally and write modifications are queued in a persistent transaction queue.

This standard establishes connectivity monitoring via the **Capacitor Network** bridge and transaction buffering using **Capacitor SQLite**.

---

# Purpose

This standard defines:

- Connectivity monitoring using `@capacitor/network`
- Client state indicators for offline usage
- Write-operation queueing (mutations buffering)
- Retry synchronization pipelines
- Conflict resolution strategies

---

# Connectivity Detection (Capacitor Network)

We monitor network states globally using Capacitor's Network plugin to show status updates and control API requests.

- **Library**: `@capacitor/network`.
- **Global Store**: Expose connection state via a unified Zustand network store.

```typescript
import { Network } from '@capacitor/network';
import { create } from 'zustand';

interface NetworkState {
  isConnected: boolean;
  connectionType: string;
  setConnection: (connected: boolean, type: string) => void;
}

export const useNetworkStore = create<NetworkState>((set) => ({
  isConnected: true,
  connectionType: 'unknown',
  setConnection: (connected, type) => set({ isConnected: connected, connectionType: type }),
}));

// Initialize listener in App entry point
Network.addListener('networkStatusChange', (status) => {
  useNetworkStore.getState().setConnection(status.connected, status.connectionType);
});

// Check status on startup
async function checkInitialNetwork() {
  const status = await Network.getStatus();
  useNetworkStore.getState().setConnection(status.connected, status.connectionType);
}
checkInitialNetwork();
```

---

# Mutation Queueing (Offline Writes)

When a user submits a form or edits a record while offline, we do not show network error screens. We buffer the mutation payload in our persistent SQLite storage.

- **Persistent Queue**: Write the request context (URL, HTTP Method, payload, token index, timestamp) to a database table.
- **Sync Worker**: When the Network listener detects connection restoration, trigger the sync pipeline.

```typescript
interface OfflineMutation {
  id: string;
  url: string;
  method: 'POST' | 'PUT' | 'DELETE';
  body: string; // Serialized JSON payload
  timestamp: number;
}

// Function to push to local SQLite mutation table
export async function queueMutation(mutation: Omit<OfflineMutation, 'id' | 'timestamp'>) {
  const id = crypto.randomUUID();
  const timestamp = Date.now();
  
  // Insert query execution on local SQLite wrapper
  await db.execute(
    'INSERT INTO mutation_queue (id, url, method, body, timestamp) VALUES (?, ?, ?, ?, ?)',
    [id, mutation.url, mutation.method, mutation.body, timestamp]
  );
}
```

---

# Conflict Resolution

When offline modifications sync to the server, data conflicts can arise. We define three resolution paths:

### 1. Last-Write-Wins (LWW)
- **Policy**: The client payload overrides server data if its local timestamp is newer.
- **Requirement**: Sync client device clock offsets via an NTP handshake on app boot.

### 2. Client-First / Server-First
- **Policy**: Choose one node as the absolute source of truth.

### 3. User Resolution
- **Policy**: Show an interactive modal detailing conflicts, allowing the user to select which version to save.

```text
        Connection Restored
                 │
                 ▼
       Drain Mutation Queue
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
 No Conflict        Conflict Detected
       │                   │
 Apply Change       Resolve using Policy:
                    ├── Last-Write-Wins
                    └── User Merge UI
```

---

# Client Data Prefetching & Caching

- **Query Prefetching**: Trigger TanStack Query prefetching on parent screen rendering (e.g. prefetching invoice details when rendering the list view).
- **Service Worker / WebView Caching**: Register standard browser cache profiles for static assets (images, icons, styles) inside WebViews.

---

# Anti-Patterns

❌ **Blocking UI with Full Spinners**: Preventing user interaction with global loading spinners during sync operations. Run sync tasks silently in the background, utilizing header indicators instead.

❌ **Uncontrolled Sync Loops**: Attempting to drain queues repeatedly without implementing back-off intervals, which exhausts device battery and overloads backend servers.

---

# Production Checklist

- [ ] Capacitor Network listener starts at root application initialization.
- [ ] Local mutation queue is stored securely in SQLite database.
- [ ] Network status indicator is present in the main UI layout.
- [ ] Sync retries use exponential back-off spacing.

---

# Success Criteria

The Offline architecture is successful when:
- Users can input data, edit, and navigate pages while completely disconnected.
- Local modifications sync instantly when network connection is re-established.
- Server conflicts are resolved without app crashes or database corruption.

---

# Document Status

**Document:** NES-405 — Offline Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-406 — Mobile Security**
