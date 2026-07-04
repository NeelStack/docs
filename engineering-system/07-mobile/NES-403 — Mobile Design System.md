---
document_id: NES-403
title: Mobile Design System
subtitle: Enterprise Mobile Tokens, Typography & NativeWind Style Guide
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

> **"Consistent design breeds professional products. We build a unified, high-performance styling system using design tokens and utility classes."**

---

# Executive Summary

A consistent look and feel across our mobile applications is key to the NeelStack brand identity.

This standard establishes the design system rules, colors, fonts, spacing tokens, and component guidelines for mobile. 

We standardize on **NativeWind** (Tailwind CSS for React Native) to align our mobile styling with our Next.js frontend web applications.

---

# Purpose

This standard defines:

- Styling Toolchain (NativeWind)
- Design Tokens (Color Palette, Typography, Spacing, Shadows)
- Dark Mode Architecture
- Component styling principles
- Adaptive Layout Guidelines

---

# Styling Toolchain (NativeWind)

We use **NativeWind v4+** to compile Tailwind CSS styles directly into Native StyleSheets at build time.

- **Unified Configuration**: The `tailwind.config.js` is shared or mirrored from the Web Design System to ensure identical theme tokens.
- **Rule**: Avoid inline `style={{ ... }}` objects for anything other than dynamic calculations (like coordinates from animations or gesture trackers).

### Styling Example:

```typescript
export function Card({ title, description }: { title: string; description: string }) {
  return (
    <View className="p-4 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
      <Text className="text-lg font-semibold text-slate-900 dark:text-white">
        {title}
      </Text>
      <Text className="mt-1 text-sm text-slate-500 dark:text-slate-400">
        {description}
      </Text>
    </View>
  );
}
```

---

# Design Tokens

## Spacing & Layout

Spacing must follow a strict **8px grid system** (e.g. `2px`, `4px`, `8px`, `16px`, `24px`, `32px`, `48px`, `64px`).

- Tailwind equivalents: `p-1` (4px), `p-2` (8px), `p-4` (16px), `p-6` (24px), `p-8` (32px).
- Use `gap` settings in `Flex` containers to space children instead of applying margins to each child.

## Color Palette

Colors match the NeelStack branding guidelines:

| Name | Light Hex | Dark Hex | Tailwind Class |
|---|---|---|---|
| Primary | `#0284C7` (Sky-600) | `#38BDF8` (Sky-400) | `bg-sky-600` / `dark:bg-sky-400` |
| Slate Base | `#0F172A` (Slate-900) | `#F8FAFC` (Slate-50) | `text-slate-900` / `dark:text-slate-50` |
| Background | `#F8FAFC` (Slate-50) | `#020617` (Slate-950) | `bg-slate-50` / `dark:bg-slate-950` |
| Surface | `#FFFFFF` | `#0F172A` (Slate-900) | `bg-white` / `dark:bg-slate-900` |
| Border | `#E2E8F0` (Slate-200) | `#1E293B` (Slate-800) | `border-slate-200` / `dark:border-slate-800` |

---

# Dark Mode Architecture

Mobile applications must support both Light and Dark modes.

- **Theme Engine**: Configure NativeWind using the `class` output system.
- **Provider Hook**: Use Expo's `useColorScheme` to track the OS-level theme preference.
- **Root Injection**: Set color scheme in `app/_layout.tsx`:

```typescript
import { useColorScheme } from 'react-native';
import { ThemeProvider, DarkTheme, DefaultTheme } from '@react-navigation/native';

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack />
    </ThemeProvider>
  );
}
```

---

# Typography Standards

Avoid using system font configurations directly. Define typography scales inside the tailwind settings.

- **Primary Font**: `Inter` (integrated via Expo Google Fonts).
- **Fallback**: System sans-serif.

| Style | Size | Weight | Tailwind Class |
|---|---|---|---|
| Display | 32px | Bold | `text-3xl font-bold` |
| Header 1 | 24px | Bold | `text-2xl font-bold` |
| Header 2 | 20px | Semibold | `text-xl font-semibold` |
| Body | 16px | Regular | `text-base font-normal` |
| Small | 14px | Medium | `text-sm font-medium` |

---

# Adaptive & Responsive Layouts

Mobile devices come in varying screen sizes. Layouts must be dynamic.

- **Flexbox**: Always use flex-based dimensions rather than fixed layouts.
- **Percentage Bounds**: Use percentage-based width bounds for modular sub-components.
- **Device Checks**: Use `useWindowDimensions()` to construct column layouts:

```typescript
import { useWindowDimensions } from 'react-native';

export function GridList() {
  const { width } = useWindowDimensions();
  const numColumns = width > 768 ? 3 : 1; // Basic tablet adaptation

  return (
    <FlatList
      key={numColumns} // Force component rebuild on layout change
      numColumns={numColumns}
      data={data}
      renderItem={renderItem}
    />
  );
}
```

---

# Anti-Patterns

❌ **Hardcoded Colors**: Styling using strings like `color: '#0284C7'` outside the stylesheet configuration or tailwind token map. This breaks dark mode styling.

❌ **Font Weight and Family Disconnect**: Assigning bold families (`font-bold`) without loading the matching font weight in Expo, causing layout breaks on Android.

❌ **Pixel-perfect Assumptions**: Designing screens for one specific device type (e.g. iPhone 15 Pro) without testing text wrap on smaller devices.

---

# Production Checklist

- [ ] All primary and secondary themes look clean in both Light and Dark modes.
- [ ] Font assets are pre-loaded in the root layout file.
- [ ] Adaptive components fit on small screen sizes.
- [ ] Interactive buttons have defined visual press states.
- [ ] Contrast ratios meet WCAG 2.2 AA standard.

---

# Success Criteria

The Design System is successful when:
- Adding support for Dark Mode requires no additional code other than prefixing classes with `dark:`.
- Color updates can be applied universally by editing `tailwind.config.js`.
- Custom primitives align perfectly on both iOS and Android.

---

# Document Status

**Document:** NES-403 — Mobile Design System
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-404 — State**
