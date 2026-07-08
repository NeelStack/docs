---
document_id: NES-404
title: State
subtitle: Enterprise Mobile State Management, Caching & Data Hydration Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-403 Mobile Design System
next_document: NES-405 Offline Architecture
---

# NES-404 — State

> **"State management must separate client and server state. We use Zustand for local client states and TanStack Query for server cache synchronization."**

---

# Executive Summary

Mobile applications require robust state management to handle user sessions, client configurations, offline write queues, and cached database records.

We isolate Client UI state from Server state. We use **Zustand** for local interface states and **TanStack Query** for background caching.

Additionally, to persist crucial state nodes (like login profiles and configurations) across app restarts, we configure Zustand with a storage adapter wrapping the **Capacitor Preferences** API.

---

# Purpose

This standard defines:

- Client UI State configuration via Zustand
- Server State caching via TanStack Query
- Persistence configuration using `@capacitor/preferences`
- Selector performance rules
- Async state hydration processes

---

# Client State (Zustand)

Zustand provides a lightweight, hook-based state container.

- **Store Isolation**: Keep stores small and focused on single domains (e.g., `useSessionStore`, `useThemeStore`).
- **Render Selectors**: Access store nodes using selectors to prevent components from re-rendering on unrelated state modifications.

### Store Example:
```typescript
import { create } from 'zustand';

interface SessionState {
  token: string | null;
  userId: string | null;
  isAuthenticated: boolean;
  setSession: (token: string, userId: string) => void;
  clearSession: () => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  token: null,
  userId: null,
  isAuthenticated: false,
  setSession: (token, userId) => set({ token, userId, isAuthenticated: true }),
  clearSession: () => set({ token: null, userId: null, isAuthenticated: false }),
}));
```

### Hook Consumption (With Selectors):
```tsx
// Correct: Re-renders ONLY when isAuthenticated changes
const isAuthenticated = useSessionStore((state) => state.isAuthenticated);
```

---

# Server State (TanStack Query)

We use **TanStack Query (React Query) v5+** to coordinate backend API caching, pagination, load indicators, and server modifications.

- **Configuration Defaults**:
  - `staleTime`: 5 minutes.
  - `gcTime` (Garbage Collection): 15 minutes.
- **Hook Isolation**: Wrap all endpoint requests inside custom hooks.

### Custom Query Hook Example:
```typescript
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

interface Document {
  id: string;
  title: string;
  status: string;
}

async function fetchDocuments(): Promise<Document[]> {
  const { data } = await api.get('/documents');
  return data;
}

export function useDocuments() {
  return useQuery({
    queryKey: ['documents'],
    queryFn: fetchDocuments,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}
```

---

# Store Persistence & Hydration

To save selected user configurations across app closures, configure Zustand's `persist` middleware with the native **Capacitor Preferences** storage engine.

- **Preferences Bridge**: Capacitor Preferences utilizes native iOS `UserDefaults` and Android `SharedPreferences`.
- **Storage Adapter**: Write a wrapper conforming to Zustand's `StateStorage` contract:

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage, StateStorage } from 'zustand/middleware';
import { Preferences } from '@capacitor/preferences';

// Adapt Capacitor Preferences to Zustand StateStorage signature
const capacitorStorage: StateStorage = {
  getItem: async (name: string): Promise<string | null> => {
    const { value } = await Preferences.get({ key: name });
    return value;
  },
  setItem: async (name: string, value: string): Promise<void> => {
    await Preferences.set({ key: name, value });
  },
  removeItem: async (name: string): Promise<void> => {
    await Preferences.remove({ key: name });
  },
};

interface SettingsState {
  notificationsEnabled: boolean;
  setNotifications: (enabled: boolean) => void;
}

export const useSettingsStore = create()(
  persist(
    (set) => ({
      notificationsEnabled: true,
      setNotifications: (enabled) => set({ notificationsEnabled: enabled }),
    }),
    {
      name: 'settings-store',
      storage: createJSONStorage(() => capacitorStorage),
    }
  )
);
```

---

# Anti-Patterns

❌ **Storing API Results in Zustand**: Duplicating backend API data inside local client stores. Use TanStack Query's cache pool instead.

❌ **Bypassing Selectors**: Calling store variables via destructuring (`const { token } = useSessionStore()`), causing unnecessary component re-renders when other attributes change.

---

# Production Checklist

- [ ] Persistent stores use the custom `capacitorStorage` adapter.
- [ ] Selectors are declared on all Zustand hook invocations.
- [ ] Query keys are array structured with dynamic parameters (e.g. `['document', id]`).
- [ ] Load and error states are handled in all screens consuming TanStack query hooks.

---

# Success Criteria

The State implementation is successful when:
- App states survive backgrounding and native application restarts.
- Consuming screens trigger low component render counts.
- Server data fetches once and is cached efficiently across client paths.

---

# Document Status

**Document:** NES-404 — State
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-405 — Offline Architecture**
