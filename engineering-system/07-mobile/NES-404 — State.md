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

> **"State management must separate client and server state. We use Zustand for UI/client state and TanStack Query for cache orchestration."**

---

# Executive Summary

Mobile applications must handle UI states, session data, user profiles, backend caches, and offline synchronization. 

Unstructured state propagation causes memory leaks, high render counts, stale displays, and inconsistent user flows.

This standard establishes the data lifecycle flow for mobile, dividing state into **Client State** and **Server State** with clear cache policies.

---

# Purpose

This standard defines:

- Client State Management (Zustand)
- Server Cache Management (TanStack Query)
- Store Isolation and Lifecycle
- Async State & Optimization (Selectors)
- Persisted States & Hydration

---

# Client State (Zustand)

We use **Zustand** as the lightweight manager for local UI state, user sessions, theme preferences, and transient states.

### Standard rules:
- **Small, Focused Stores**: Avoid single giant states. Keep stores isolated by domain (e.g. `useAuthStore`, `useSettingsStore`).
- **Use Selectors**: Always use selectors when consuming states to prevent unnecessary re-rendering.

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

### Component Selector Consumption:

```typescript
// Correct: Only re-renders if isAuthenticated changes
const isAuthenticated = useSessionStore((state) => state.isAuthenticated);
```

---

# Server State (TanStack Query)

We use **TanStack Query (React Query) v5+** to manage server caching, loading states, retry logic, and background synchronization.

### Standard configurations:
- **Global Defaults**:
  - `staleTime`: 5 minutes (default cache lifetime before re-querying in the background).
  - `gcTime`: 15 minutes (garbage collection window for unused query nodes).
- **Custom Hooks**: Wrap every endpoint fetch in a custom query hook.

### Hook Example:

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

Selected client states must persist across app reboots (e.g., login tokens, user preferences).

- **Storage Engine**: Configure Zustand with `persist` middleware using a custom wrapper around `expo-secure-store` or `async-storage`.
- **Hydration Safety**: Because state hydration runs asynchronously on app startup, ensure components display a loader until hydration completes:

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const useSettingsStore = create()(
  persist(
    (set) => ({
      notificationsEnabled: true,
      setNotifications: (enabled: boolean) => set({ notificationsEnabled: enabled }),
    }),
    {
      name: 'settings-store',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

---

# Cache Invalidation & Mutations

When modifying backend resources, immediately update or invalidate related queries.

- **Query Invalidation**: Use `queryClient.invalidateQueries` inside mutation success handlers.
- **Optimistic Updates**: For critical actions (e.g. archiving a document), perform optimistic UI updates to ensure the interface responds instantly, rolling back on failure.

---

# Anti-Patterns

❌ **Mixing State Types**: Storing backend server responses in a Zustand client store. This creates duplicate caches and causes sync issues.

❌ **Missing Selectors**: De-structuring states directly like `const { userId, token } = useSessionStore()`, which forces the component to re-render on *any* property change in that store.

❌ **Blocking App Mounting**: Blocking the app from loading while fetching non-essential configurations. Use loaders or screen splash flags until core hydration finishes.

---

# Production Checklist

- [ ] All Zustand persistent stores have a defined `storage` configuration.
- [ ] Selectors are used on every single state hook call.
- [ ] TanStack Query keys are configured as arrays with dynamic parameters (e.g. `['documents', id]`).
- [ ] Mutation error cases have user-facing warning banners.
- [ ] Garbage collection times are checked to prevent memory leaks on low-end devices.

---

# Success Criteria

The State setup is successful when:
- App state is consistent when backgrounding and resuming the app.
- Component render counts remain low during rapid state changes.
- Stored session states are decrypted and loaded safely on startup.
- Backend responses are fetched once and shared across screens automatically.

---

# Document Status

**Document:** NES-404 — State
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-405 — Offline Architecture**
