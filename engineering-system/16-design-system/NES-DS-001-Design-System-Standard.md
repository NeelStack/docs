---
document_id: NES-DS-001
title: NeelStack Design System Standard
subtitle: The unified design system governing all visual and interaction design across NeelStack products
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Design System Team
review_cycle: Every 6 Months
document_type: Engineering Standard
---

# NES-DS-001 — NeelStack Design System Standard

> **"Design is not decoration. Design is function made visible. A consistent design system makes every product feel like one product."**

---

# Executive Summary

The NeelStack Design System is the single source of truth for all visual, interaction, and component design across EduOS, Toolvines, DhruvaOS, NaukariMitra, and SarkariMitra.

Every product team consuming the design system writes less CSS, ships faster, and delivers a consistent user experience.

---

# Design Tokens

Design tokens are the atomic values that drive all visual decisions.

## Color Palette

```css
:root {
  /* Brand Colors */
  --color-brand-primary: #4F46E5;     /* Indigo 600 */
  --color-brand-secondary: #7C3AED;   /* Violet 600 */
  --color-brand-accent: #06B6D4;      /* Cyan 500 */

  /* Semantic Colors */
  --color-success: #10B981;           /* Emerald 500 */
  --color-warning: #F59E0B;           /* Amber 500 */
  --color-error: #EF4444;             /* Red 500 */
  --color-info: #3B82F6;              /* Blue 500 */

  /* Neutral Scale */
  --color-neutral-50: #F9FAFB;
  --color-neutral-100: #F3F4F6;
  --color-neutral-200: #E5E7EB;
  --color-neutral-500: #6B7280;
  --color-neutral-700: #374151;
  --color-neutral-900: #111827;

  /* Surface Colors */
  --color-surface-primary: #FFFFFF;
  --color-surface-secondary: #F9FAFB;
  --color-surface-elevated: #FFFFFF;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface-primary: #111827;
    --color-surface-secondary: #1F2937;
    --color-surface-elevated: #1F2937;
    --color-neutral-900: #F9FAFB;
  }
}
```

## Typography

```css
:root {
  /* Font Families */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Font Scale */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

## Spacing Scale

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

## Border Radius

```css
:root {
  --radius-sm: 0.25rem;   /* 4px */
  --radius-md: 0.375rem;  /* 6px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-full: 9999px;  /* pill */
}
```

---

# Core Components

## Button

Variants: `primary`, `secondary`, `ghost`, `danger`, `link`

Sizes: `sm`, `md`, `lg`

```tsx
<Button variant="primary" size="md" loading={false}>
  Enroll Now
</Button>
```

States: default, hover, active, disabled, loading

## Input

Types: `text`, `email`, `password`, `number`, `search`, `textarea`

States: default, focused, error, disabled, success

```tsx
<Input
  label="Email Address"
  type="email"
  placeholder="you@school.edu"
  error="Please enter a valid email"
/>
```

## Card

Variants: `default`, `elevated`, `outlined`, `interactive`

## Badge

Variants: `default`, `success`, `warning`, `error`, `info`

## Avatar

Sizes: `xs`, `sm`, `md`, `lg`, `xl`

Fallback: Initials when image unavailable

---

# Component Library Location

The NeelStack component library lives at `packages/ui/` in each product repository and is also published to the internal npm registry as `@neelstack/ui`.

---

# Accessibility Requirements (NES-309)

All design system components must:
- Meet **WCAG 2.2 Level AA** minimum
- Have keyboard navigation support
- Have ARIA roles and attributes
- Have focus-visible styles (not hidden focus rings)
- Have minimum color contrast ratio of 4.5:1 (text), 3:1 (UI elements)

---

# Design System Governance

- New components proposed via GitHub Issue with design mockup
- ARB + Design System Team review
- Approved components added to Figma and code simultaneously
- Deprecated components have 2-version deprecation window

---

# Related Standards

- NES-303 — Design System Architecture
- NES-304 — UI Component Standards
- NES-305 — Tailwind CSS Standards
- NES-309 — Accessibility Standards
- TECH-002 — Next.js Standard

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial design system standard |
