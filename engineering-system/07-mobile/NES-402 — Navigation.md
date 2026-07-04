---
document_id: NES-402
title: Navigation
subtitle: Enterprise Expo Router, Navigation & Deep Linking Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-401 Expo Architecture
next_document: NES-403 Mobile Design System
---

# NES-402 — Navigation

> **"Navigation defines the user flow of a mobile application. We use Expo Router to build file-based, type-safe, and deep-linkable routing structures."**

---

# Executive Summary

Mobile routing requires careful management of navigation state, UI stacks, modals, tab views, and deep link pathways.

NeelStack standardizes on **Expo Router**—a file-based router built on top of React Navigation—to ensure that our mobile routing is predictable, intuitive, and shares similar design paradigms with our Next.js frontend applications.

---

# Purpose

This standard defines:

- Router Directory Structure
- Type-Safe Routing and Links
- Navigation Types (Tabs, Stacks, Modals, Drawers)
- Parameter Management and Validation
- Deep Linking Configuration

---

# Router Directory Structure

Expo Router uses the filesystem structure inside the `/app` directory to define routes:

```text
app/
├── _layout.tsx           # Global provider layout (Auth, Contexts)
├── index.tsx             # Entry route (Splash / Redirection logic)
├── (auth)/               # Auth group
│   ├── _layout.tsx       # Auth stack layout (Header options)
│   ├── login.tsx         # Login Screen
│   └── register.tsx      # Register Screen
├── (app)/                # Authenticated application group
│   ├── _layout.tsx       # Main tab/drawer layout
│   ├── (tabs)/           # Tab navigation
│   │   ├── _layout.tsx   # Tabs layout
│   │   ├── home.tsx      # Home Tab
│   │   └── profile.tsx   # Profile Tab
│   └── document/         # Document details stack
│       └── [id].tsx      # Dynamic route: /document/123
└── modal.tsx             # Global modal screen
```

---

# Navigation Paradigms

## Stacks

Stack layouts handle linear screen transitions (push/pop).
Declare them in layouts explicitly to control headers, gestures, and animations:

```typescript
import { Stack } from 'expo-router';

export default function Layout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: '#1A202C' },
        headerTintColor: '#FFF',
        headerTitleStyle: { fontWeight: 'bold' },
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen name="(auth)" options={{ headerShown: false }} />
      <Stack.Screen name="(app)" options={{ headerShown: false }} />
      <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
    </Stack>
  );
}
```

## Tabs

Tabs represent primary app destinations.
Use bottom tabs with native configurations:

```typescript
import { Tabs } from 'expo-router';

export default function TabsLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="home" options={{ title: 'Home' }} />
      <Tabs.Screen name="profile" options={{ title: 'Profile' }} />
    </Tabs>
  );
}
```

---

# Type-Safe Linkage

All links must be navigated using the Expo Router `Link` component or the `router` imperative hook.

### Component Usage:

```typescript
import { Link } from 'expo-router';

export function NavigationButton() {
  return (
    <Link href="/document/456" asChild>
      <Pressable>
        <Text>View Document</Text>
      </Pressable>
    </Link>
  );
}
```

### Imperative Hook:

```typescript
import { useRouter } from 'expo-router';

export function ActionButton() {
  const router = useRouter();

  const handleAction = () => {
    // Perform logic
    router.push({
      pathname: '/document/[id]',
      params: { id: '789' }
    });
  };

  return <Button title="Go" onPress={handleAction} />;
}
```

---

# Parameter Handling and Validation

Dynamic parameters must be parsed and typed using Schema Validation (`zod`) to avoid undefined exceptions in detail views.

```typescript
import { useLocalSearchParams } from 'expo-router';
import { z } from 'zod';

const paramSchema = z.object({
  id: z.string().uuid(),
});

export default function DocumentDetailsScreen() {
  const params = useLocalSearchParams();
  
  const validation = paramSchema.safeParse(params);
  if (!validation.success) {
    return <Text>Invalid Document ID</Text>;
  }

  const { id } = validation.data;
  return <Text>Document ID: {id}</Text>;
}
```

---

# Deep Linking Configuration

Deep linking configuration is unified inside `app.config.js` via the `scheme` property and the `expo-router` custom setup.

- **Uniform Resource Scheme**: The primary scheme is `neelstack://`.
- **Universal Links (iOS/Android)**: Map web-based routes (e.g. `https://portal.neelstack.com/document/123`) to mobile screens automatically by configuring iOS `associatedDomains` and Android `intentFilters` inside `app.config.js`.

---

# Anti-Patterns

❌ **Hardcoded Routing Helpers**: Writing custom routing utility layers that bypass Expo Router, which breaks type safety and deep links.

❌ **Over-nesting Group Folders**: Creating excessive directory groups (`(group1)/(group2)/(group3)`) which makes folder mapping and code navigation highly confusing.

❌ **Passing Complex Objects in Params**: Serializing large JSON payloads as string parameters in links. Pass the ID only, and fetch/retrieve data from cache or store in the target screen.

---

# Production Checklist

- [ ] All dynamic routes validate inputs via Zod.
- [ ] Transition animations conform to platform standards.
- [ ] Safe Areas are respected inside dynamic header settings.
- [ ] URL schemas are mapped and tested.
- [ ] Dynamic Universal Link routing works when the app is backgrounded.

---

# Success Criteria

The Navigation design is successful when:
- Adding a new screen simply involves creating a file in `/app` and it automatically gets typed.
- Deep links navigate directly to the correct nested target screen when the application is launched from a cold state.
- Screen transitions execute smoothly at 60 FPS without layout shifts.

---

# Document Status

**Document:** NES-402 — Navigation
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-403 — Mobile Design System**
