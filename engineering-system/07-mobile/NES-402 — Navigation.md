---
document_id: NES-402
title: Navigation
subtitle: Enterprise React Router, Mobile Web Navigation & Deep Linking Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-401 Capacitor Architecture
next_document: NES-403 Mobile Design System
---

# NES-402 — Navigation

> **"Navigation manages the client execution flow. We use React Router v7 to build clean, browser-compatible SPA routes, handling physical hardware back events and deep link schemes at the bridge level."**

---

# Executive Summary

In a hybrid mobile web application, navigation runs within a single-page application (SPA) container.

We standardize on **React Router Dom v7** as our routing engine, wrapping transitions, tab groups, stacks, and modals in standard DOM navigation pathways.

Additionally, we intercept native device events (like the Android hardware back button and system deep link invokes) via the Capacitor core bridge to sync native operations with the web router.

---

# Purpose

This standard defines:

- Single Page Application (SPA) routing layouts
- Routing Configuration and nested routes structure
- Handling Android Hardware Back Button events
- Deep Link interception and path routing
- Parameter extraction and type validation

---

# Routing Directory Structure

We organize routes inside the `src/` directory to manage public, private, and nested layout views:

```text
src/
├── routes/
│   ├── layouts/
│   │   ├── AuthLayout.tsx     # Layout wrapper for authentication routes
│   │   ├── AppLayout.tsx      # Main tab/navigation wrapper layout
│   │   └── RootLayout.tsx     # Global providers (Auth, Theme)
│   ├── auth/
│   │   ├── Login.tsx          # /login screen
│   │   └── Register.tsx       # /register screen
│   ├── app/
│   │   ├── Home.tsx           # /app/home tab
│   │   ├── Profile.tsx        # /app/profile tab
│   │   └── document/
│   │       └── Detail.tsx     # Dynamic detail: /app/document/:id
│   └── index.ts               # Routing definitions tree
```

---

# React Router v7 Configuration

We declare our routes structure inside a centralized router module:

```typescript
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { RootLayout } from './routes/layouts/RootLayout';
import { AuthLayout } from './routes/layouts/AuthLayout';
import { AppLayout } from './routes/layouts/AppLayout';
import { Login } from './routes/auth/Login';
import { Home } from './routes/app/Home';
import { Profile } from './routes/app/Profile';
import { DocumentDetail } from './routes/app/document/Detail';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        element: <AuthLayout />,
        children: [
          { path: 'login', element: <Login /> },
        ]
      },
      {
        path: 'app',
        element: <AppLayout />,
        children: [
          { path: 'home', element: <Home /> },
          { path: 'profile', element: <Profile /> },
          { path: 'document/:id', element: <DocumentDetail /> },
        ]
      },
      { path: '*', element: <Navigate to="/app/home" replace /> }
    ]
  }
]);
```

---

# Android Hardware Back Button Handling

Android devices include a physical back button. By default, tapping this inside a WebView can cause the application to exit or break. We use the Capacitor App plugin to route back button actions through React Router.

- **Library**: `@capacitor/app`.
- **Implementation**: Hook back button events in the root layout:

```typescript
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { App } from '@capacitor/app';

export function useBackButtonHandler() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handler = App.addListener('backButton', ({ canGoBack }) => {
      if (location.pathname === '/app/home' || location.pathname === '/login') {
        // Exit the app if on primary landing roots
        App.exitApp();
      } else {
        // Go back in router history
        navigate(-1);
      }
    });

    return () => {
      handler.then(h => h.remove());
    };
  }, [location, navigate]);
}
```

---

# Deep Linking & Universal Links

Deep linking matches scheme urls (e.g. `neelstack://app/document/123`) to router paths.

- **Bridge Listener**: Capture incoming URLs via the Capacitor App listener and dispatch them into React Router.

```typescript
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { App } from '@capacitor/app';

export function useDeepLinkHandler() {
  const navigate = useNavigate();

  useEffect(() => {
    const handler = App.addListener('appUrlOpen', (event) => {
      // Parse link domain and path
      // Example event.url: "neelstack://app/document/123"
      const slug = event.url.split('neelstack://')[1];
      if (slug) {
        navigate(`/${slug}`);
      }
    });

    return () => {
      handler.then(h => h.remove());
    };
  }, [navigate]);
}
```

Ensure native app profiles configuration:
- **iOS**: Map Associated Domains (`applinks:portal.neelstack.com`) and URL Scheme (`neelstack`).
- **Android**: Configure intent filters for the custom scheme and site URL inside `AndroidManifest.xml`.

---

# Parameter Handling and Validation

Extract dynamic query segments using `useParams` and validate parameters via `zod` schemas to prevent crashes from invalid IDs:

```typescript
import { useParams } from 'react-router-dom';
import { z } from 'zod';

const idParamSchema = z.object({
  id: z.string().uuid(),
});

export function DocumentDetail() {
  const params = useParams();
  
  const validation = idParamSchema.safeParse(params);
  if (!validation.success) {
    return <div className="p-4 text-red-600">Invalid Document Reference</div>;
  }

  const { id } = validation.data;
  return <div className="p-4">Loading Document: {id}</div>;
}
```

---

# Anti-Patterns

❌ **Direct window.location Mutation**: Bypassing React Router to change window URLs, causing full page reloads and clearing global memory/state inside the WebView.

❌ **Ignoring Android Back Events**: Forgetting to register backButton listeners, which triggers app suspension or closes the app when a user taps "back" inside a detail view.

❌ **Over-nesting Group Elements**: Constructing overly nested routing segments that make deep link parsing complex.

---

# Production Checklist

- [ ] Android back button exits only on root pages; navigates back on details.
- [ ] Deep links navigate directly to active sub-routes from a cold launch.
- [ ] Route parameters are strictly typed and validated via Zod.
- [ ] Safe Area top/bottom padding surrounds header and bottom tabs navigation.

---

# Success Criteria

The Navigation standard is successful when:
- Creating a route simply involves declaring it in `routes/index.ts` and adding a matching view file.
- Single Page transitions occur instantly without screen flashes.
- Web URL paths map directly to mobile client navigation routes via deep linking.

---

# Document Status

**Document:** NES-402 — Navigation
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-403 — Mobile Design System**
