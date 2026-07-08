---
document_id: NES-403
title: Mobile Design System
subtitle: Enterprise Web Standards, Safe-Areas & Tailwind CSS Style Guide
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Design & Architecture Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-402 Navigation
next_document: NES-404 State
---

# NES-403 — Mobile Design System

> **"A unified styling system maximizes UI reuse. We design our Capacitor mobile views using standard Tailwind CSS and semantic HTML, ensuring fluid responsive layouts and secure notch safe areas."**

---

# Executive Summary

Because Capacitor compiles web assets into native WebViews, we have no need for complex native styling wrappers like NativeWind. We write standard, clean HTML5 and styled Tailwind CSS code.

This standard outlines spacing tokens, custom safe areas for modern screens (notches, status bars), typography scales, dynamic dark mode, and responsive layout guidelines for our hybrid mobile applications.

---

# Purpose

This standard defines:

- Styling toolchain (Tailwind CSS v3 web integration)
- Notch and device safe areas configuration
- Dark Mode styling setup
- Typography tokens
- Multi-device layout standards

---

# Styling Toolchain (Tailwind CSS)

We use standard **Tailwind CSS v3** in our mobile React applications.

- **Unified Configuration**: Mirror the web design system configuration inside `tailwind.config.js` to ensure uniform colors, borders, and margins.
- **Rules**:
  - Avoid inline styles (`style={{ ... }}`) unless rendering dynamic, runtime-calculated properties (e.g., card gestures, drag-and-drop coordinates).
  - Use standard HTML tags (`div`, `header`, `main`, `section`, `span`, `button`).

### Component Example:
```tsx
export function Card({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors duration-200">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
        {title}
      </h3>
      <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
        {description}
      </p>
    </div>
  );
}
```

---

# Notch & Device Safe Areas

Mobile devices have camera notches, status bars, and bottom gesture home bars. Web content must not bleed under these areas.

- **CSS Environment Variables**: Use standard CSS environment variables.
- **Utility Setup**: Define custom padding classes inside `src/index.css`:

```css
/* In index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer utilities {
  .safe-top {
    padding-top: env(safe-area-inset-top, 0px);
  }
  .safe-bottom {
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }
  .safe-height {
    height: calc(100dvh - env(safe-area-inset-top, 0px) - env(safe-area-inset-bottom, 0px));
  }
}
```

- **Usage**: Apply `.safe-top` to headers and `.safe-bottom` to bottom tab navigation bars or screen footers.

---

# Dark Mode Architecture

Our mobile applications inherit light/dark configurations from standard media queries or class selections:

- **Theme Engine**: Configure Tailwind CSS with the `class` selector option inside `tailwind.config.js`.
- **System Sync**: Check system themes or user session preferences and apply the `dark` class to the `<html>` root node:

```typescript
import { useEffect } from 'react';

export function useThemeSync() {
  useEffect(() => {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);
}
```

---

# Typography Standards

We use standard typography classes bound to the Inter Google font.

| Style | Size | Weight | Tailwind Class |
|---|---|---|---|
| Display | 32px | Bold | `text-3xl font-bold` |
| Header 1 | 24px | Bold | `text-2xl font-bold` |
| Header 2 | 20px | Semibold | `text-xl font-semibold` |
| Body | 16px | Regular | `text-base font-normal` |
| Small | 14px | Medium | `text-sm font-medium` |

---

# Adaptive & Responsive Layouts

To adapt layouts across phone and tablet WebView environments:

- **Viewport Sizing**: Enforce dynamic viewport heights (`dvh`, `lvh`) instead of standard `vh` to prevent mobile address bar/keyboard sizing mismatches.
- **Flex and Grid**: Leverage Tailwind Flexbox and Grid layouts to align columns and scale tables dynamically.
- **Media Queries**: Utilize responsive breakpoints (`md:`, `lg:`) to display multi-column grids on tablets.

```tsx
export function DocumentGrid({ items }: { items: any[] }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4">
      {items.map(item => (
        <Card key={item.id} title={item.title} description={item.status} />
      ))}
    </div>
  );
}
```

---

# Anti-Patterns

❌ **Hardcoded Top/Bottom Margins**: Using static margins like `mt-12` for headers, which leaves headers under the status bar on notched devices, or too low on bezel-based displays. Use `.safe-top`.

❌ **Fixed Pixels Sizing**: Assigning absolute width values (e.g. `w-[375px]`) that break UI consistency on smaller Android devices or when rendering on larger tablets.

---

# Production Checklist

- [ ] Header layouts and navigation drawers respect device top notches.
- [ ] UI colors and contrast ratios pass accessibility checks in both modes.
- [ ] Viewport height is dynamic (`dvh`) to avoid footer cutoff when virtual keyboards show.
- [ ] All clickable items have hover and active press styles.

---

# Success Criteria

The Design System is successful when:
- Layout and component UI codebase are 100% shared between web console and mobile platforms.
- Supporting dark mode only requires applying standard `dark:` class utilities.
- Safe Area offsets render perfectly on all emulator models tested.

---

# Document Status

**Document:** NES-403 — Mobile Design System
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-404 — State**
