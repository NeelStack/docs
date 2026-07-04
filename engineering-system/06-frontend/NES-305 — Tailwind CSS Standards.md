---
document_id: NES-305
title: Tailwind CSS Standards
subtitle: Enterprise Tailwind CSS Architecture, Styling & Design Token Standards
version: 1.0.0
status: Draft
classification: Internal
owner: Frontend Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-304 UI Component Standards
next_document: NES-306 State Management Standards
---

# NES-305 — Tailwind CSS Standards

> **"CSS should be predictable, scalable, token-driven, and invisible to product teams."**

---

# Executive Summary

This document defines the official Tailwind CSS standards for every NeelStack web application.

The goal is to establish a unified styling architecture that is

- Consistent
- Maintainable
- Themeable
- Performant
- Accessible
- Responsive
- Design Token Driven

Tailwind CSS is the official styling framework across all React and Next.js applications.

Custom CSS should be the exception—not the rule.

---

# Purpose

This document defines

- Tailwind Architecture
- Styling Principles
- Design Token Integration
- Utility Standards
- Responsive Design
- Dark Mode
- Component Styling
- Custom Utilities
- Performance
- Governance

---

# Vision

Build a styling platform capable of supporting

- Hundreds of Applications

- Thousands of Components

- Multiple Brands

- Multi-Tenant Themes

- AI-Native Interfaces

through one consistent design language.

---

# Tailwind Philosophy

```text
Design Tokens

↓

Tailwind Theme

↓

Utilities

↓

Components

↓

Layouts

↓

Applications
```

Everything begins with design tokens.

---

# Core Principles

Every UI must be

✓ Utility First

✓ Token Driven

✓ Responsive

✓ Accessible

✓ Themeable

✓ Predictable

✓ Reusable

✓ Performant

✓ Minimal CSS

---

# Official Stack

Framework

```
Tailwind CSS Latest Stable
```

Plugins

```
tailwindcss-animate

@tailwindcss/forms

@tailwindcss/typography

@tailwindcss/container-queries
```

Component Library

```
shadcn/ui
```

Icons

```
Lucide React
```

---

# Architecture

```text
Design Tokens

↓

Tailwind Config

↓

Utilities

↓

Component Classes

↓

Application UI
```

---

# Styling Hierarchy

```text
Design Tokens

↓

Base Styles

↓

Utilities

↓

Components

↓

Layouts

↓

Pages
```

---

# Design Token Integration

Tailwind configuration consumes

Colors

Typography

Spacing

Radius

Border

Shadows

Opacity

Animations

Breakpoints

Z-Index

Tokens remain the source of truth.

---

# Color Standards

Use semantic colors only

Good

```text
bg-primary

text-primary

border-border

bg-muted

text-destructive
```

Avoid

```text
bg-blue-500

text-red-700

bg-green-300
```

Applications never reference raw palette values.

---

# Typography

Use semantic utilities

```
text-xs

text-sm

text-base

text-lg

text-xl

text-2xl
```

Never define arbitrary font sizes repeatedly.

---

# Spacing Standards

Official spacing scale

```
1

2

3

4

5

6

8

10

12

16

20

24

32
```

Based on the 4px spacing grid.

Avoid arbitrary values.

---

# Layout Standards

Preferred utilities

```
flex

grid

container

gap

space-x

space-y

justify

items
```

Avoid float-based layouts.

---

# Width & Height

Preferred

```text
w-full

max-w-screen-xl

min-h-screen

h-full
```

Avoid hardcoded pixel dimensions unless necessary.

---

# Responsive Design

Official breakpoints

```text
sm

md

lg

xl

2xl
```

Always build mobile first.

Example

```html
<div class="w-full md:w-1/2 lg:w-1/3">
```

---

# Dark Mode

Official strategy

```
class
```

Support

Light

Dark

System

Never duplicate components.

---

# State Styling

Support

Hover

Focus

Active

Disabled

Loading

Open

Selected

Example

```html
hover:bg-primary

focus:ring-2

disabled:opacity-50
```

---

# Variant Standards

Variants include

Primary

Secondary

Outline

Ghost

Destructive

Success

Warning

Link

Variants map to semantic tokens.

---

# Border Radius

Official scale

```
rounded-none

rounded-sm

rounded-md

rounded-lg

rounded-xl

rounded-2xl

rounded-full
```

---

# Shadows

Official shadows

```
shadow-sm

shadow

shadow-md

shadow-lg

shadow-xl
```

Avoid custom shadow values.

---

# Z-Index

Official scale

```
z-0

z-10

z-20

z-30

z-40

z-50
```

Avoid arbitrary z-index values.

---

# Animation

Official library

```
tailwindcss-animate
```

Support

Fade

Slide

Scale

Accordion

Loading

Dialog

Respect

```
prefers-reduced-motion
```

---

# Utility Standards

Prefer

```html
flex items-center gap-2
```

Avoid unnecessary wrapper classes.

Keep utility combinations readable.

---

# Class Ordering

Official order

```text
Layout

↓

Spacing

↓

Sizing

↓

Typography

↓

Colors

↓

Borders

↓

Effects

↓

State

↓

Animation
```

Example

```html
flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-md bg-primary text-primary-foreground hover:bg-primary/90
```

---

# Class Composition

Use

```
cn()
```

for conditional classes.

Example

```tsx
cn(

"rounded-md",

variant === "primary" && "bg-primary"

)
```

Never concatenate class strings manually.

---

# Component Styling

Every component uses

```tsx
className={cn(...)}
```

Component variants use

```
class-variance-authority (CVA)
```

---

# CVA Standards

Use CVA for

Variants

Sizes

States

Themes

Example

```tsx
buttonVariants({

variant:"primary",

size:"md"

})
```

---

# Custom CSS

Allowed only for

Third-party Overrides

Complex Animations

Print Styles

Browser Workarounds

Everything else uses utilities.

---

# Global CSS

Only

```
globals.css
```

may contain

Tailwind Imports

CSS Variables

Reset

Font Definitions

Scrollbar

Selection

No business styles.

---

# CSS Variables

Store

Colors

Spacing

Radius

Typography

Motion

Themes

Never hardcode values.

---

# Accessibility

Support

Focus Rings

High Contrast

Dark Mode

Reduced Motion

Touch Targets

Keyboard Navigation

---

# Performance

Optimize

Tree Shaking

Purge

Minimal CSS

Utility Reuse

No Dead Styles

Small Bundle Size

---

# AI UI Styling

Support

Streaming Messages

Markdown

Code Blocks

Tool Status

Citations

Reasoning Timeline

Typing Indicators

Human Approval

Following NES-218 through NES-230.

---

# Folder Structure

```text
styles/

├── globals.css

├── tokens.css

├── themes.css

├── utilities.css

├── animations.css

├── typography.css

└── print.css
```

---

# Tailwind Configuration

```text
tailwind.config.ts

↓

Theme

↓

Plugins

↓

Content

↓

Safelist

↓

Container

↓

Dark Mode
```

Configuration remains centralized.

---

# Enterprise Package Structure

```text
packages/

├── tailwind-config/

├── design-tokens/

├── themes/

├── ui/

├── motion/

└── icons/
```

---

# Linting Rules

Disallow

Duplicate Classes

Arbitrary Colors

Unused CSS

Deep Nesting

Important Overrides

Inconsistent Ordering

Tailwind linting is mandatory.

---

# Testing

Validate

Dark Mode

Responsive Layout

Accessibility

Visual Regression

Cross-browser Rendering

Theme Switching

---

# Governance

Styling changes require

Design Review

↓

Architecture Review

↓

Visual Testing

↓

Accessibility Review

↓

Release

---

# KPIs

Utility Reuse

```
>95%
```

Global CSS

```
<5%
```

Theme Coverage

```
100%
```

Dark Mode Support

```
100%
```

Visual Regression Failures

```
0
```

---

# Anti-Patterns

Avoid

❌ Inline Styles

❌ Raw Hex Colors

❌ Custom CSS for Common Layouts

❌ Arbitrary Spacing

❌ Arbitrary Font Sizes

❌ Multiple Theme Implementations

❌ Duplicate Utilities

❌ CSS Modules for Shared Components

❌ !important Overrides

❌ Styling Without Tokens

---

# Production Checklist

Before production

- [ ] Tailwind configuration validated
- [ ] Design tokens integrated
- [ ] CVA used for variants
- [ ] Responsive layouts verified
- [ ] Dark mode tested
- [ ] Accessibility validated
- [ ] Visual regression completed
- [ ] CSS bundle optimized
- [ ] Documentation updated
- [ ] Architecture review approved

---

# Success Criteria

Tailwind CSS Standards are successful when

- Every application shares a common styling language.
- Components rely exclusively on design tokens.
- Themes switch without component changes.
- CSS remains minimal and maintainable.
- Responsive layouts are consistent.
- Accessibility is built into styling.
- Developers move quickly without custom CSS.
- UI remains visually consistent across every product.

---

# Future Evolution

Version 2.0 will include

- Tailwind CSS v5 Migration Guide
- Enterprise Theme Engine
- W3C Design Token Pipeline
- Multi-Brand Styling Architecture
- Advanced Container Query Patterns
- AI-Native Styling Utilities
- Motion Design Utility Library
- CSS Performance Dashboard
- Enterprise Tailwind Plugin Collection
- Storybook Theme Integration
- C4 Styling Architecture
- Architecture Fitness Rules for Styling
- Production Tailwind Enterprise Starter Repository

---

# Tailwind CSS Standards Checklist

- [x] Styling Architecture Defined
- [x] Design Token Integration Established
- [x] Utility Standards Defined
- [x] Responsive Standards Included
- [x] Theme Architecture Defined
- [x] CVA Standards Included
- [x] Performance Standards Defined
- [x] Accessibility Requirements Included
- [x] Production Checklist Added
- [x] Success Criteria Defined

---

# Document Status

**Document:** NES-305 — Tailwind CSS Standards

**Version:** 1.0.0

**Status:** Ready for Architecture Review

**Next Document:** **NES-306 — State Management Standards**

---

# Revision Queue for Version 2.0 (Enterprise Edition)

Future enhancements will include

- Tailwind CSS v5 Enterprise Migration Guide
- Enterprise Theme Engine Reference Architecture
- W3C Design Tokens Pipeline Integration
- CVA Enterprise Component Patterns
- Multi-Brand Styling Framework
- AI-Native UI Utility Library
- Motion & Animation Architecture
- CSS Performance Benchmark Suite
- Enterprise Tailwind Plugin Ecosystem
- Storybook Theme Automation
- C4 Context, Container & Styling Diagrams
- Architecture Fitness Tests for CSS Architecture
- Production Enterprise Tailwind Starter Repository

These enhancements will establish the definitive Tailwind CSS Standard for the NeelStack ecosystem, ensuring every application delivers consistent, accessible, high-performance, token-driven styling with minimal custom CSS and a scalable foundation for enterprise UI development.