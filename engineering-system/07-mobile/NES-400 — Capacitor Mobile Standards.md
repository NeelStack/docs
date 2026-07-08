---
document_id: NES-400
title: Capacitor Mobile Standards
subtitle: Enterprise React, Mobile Web Hybrid Architecture & Development Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-320 Frontend Reference Architecture
next_document: NES-401 Capacitor Architecture
---

# NES-400 — Capacitor Mobile Standards

> **"Single codebase, web platform speed, native container integration. We write hybrid mobile web applications that render beautifully and run efficiently inside native WebViews."**

---

# Executive Summary

Mobile applications are a critical touchpoint for NeelStack customers.

To deliver high-performance, secure, and responsive hybrid applications on both iOS and Android, we standardize on **Capacitor** as our primary mobile container framework. 

This document defines the core architecture, coding practices, typescript rules, component lifecycle conventions, and platform-specific guidelines for building Capacitor-based mobile applications at NeelStack.

Every mobile project must adhere to these standards to ensure long-term maintainability and high developer velocity.

---

# Purpose

This standard establishes:

- Core mobile web technologies and packages
- TypeScript conventions for mobile web components
- Component structure and code organization
- WebView vs. Native bridge execution principles
- iOS and Android platform UI consistency guidelines
- Code quality, formatting, and linting configurations

---

# Core Principles

Every Capacitor mobile web application must be:

✓ **WebView-Optimized**: Render layouts smoothly without heavy reflows or repaints.

✓ **Type Safe**: End-to-end typing from API requests to React component props.

✓ **Performant**: Minimize bundle sizes, optimize asset loading, and use hardware-accelerated CSS animations.

✓ **Observable**: Capture crashes, telemetry, and analytical events reliably.

✓ **Maintainable**: Keep styles, state, and UI logic modular and isolated.

---

# Tech Stack & Package Standards

We lock specific library versions to prevent fragmentation across mobile products:

| Area | Approved Library | Rationale |
|---|---|---|
| Core Framework | React 19 + Vite 6 | Fast compilation, modern React hooks support |
| Mobile Container | Capacitor v7 | Standardized bridge to native APIs (Camera, storage, FCM) |
| Styling | Tailwind CSS v3 | Utility CSS styling matching design system |
| State | Zustand + TanStack Query | Client & server state isolation |
| Navigation | React Router Dom v7 | Standard single page application client routing |
| Icons | Lucide React | Lightweight vector icons |

---

# Coding Standards & Guidelines

## TypeScript Configuration

All code must be written in TypeScript with strict null checks enabled.

- Avoid the `any` type at all costs. Use `unknown` with type guards if the type is dynamic.
- Declare prop interfaces explicitly for every component.

```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false,
}) => {
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className={`px-4 py-2 rounded ${variant === 'primary' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-black'}`}
    >
      {label}
    </button>
  );
};
```

---

# Component Best Practices

1. **Use Functional Components**: Class components are legacy and prohibited.
2. **Minimize DOM Nodes**: Keep DOM tree depth shallow to optimize rendering and scroll performance inside the WebView.
3. **Prefer Web Standards**: Use standard HTML5 tags (`div`, `section`, `span`, `button`) styled via Tailwind CSS class names.
4. **Use Virtualized Lists**: Avoid rendering large arrays of elements directly in the DOM. Use virtualized list libraries (such as `@tanstack/react-virtual`) or react-infinite-scroll-component for smooth performance.

---

# Platform-Specific Code Handling

To write cross-platform code while respecting platform design patterns:

- **Platform Check**: Use Capacitor's `Capacitor.getPlatform()` method to identify host operating systems.
- **CSS Safe Areas**: Leverage CSS environment variables to handle device notches and system indicators.

```css
/* In index.css */
.safe-area-top {
  padding-top: env(safe-area-inset-top, 0px);
}
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
```

---

# Thread Management & Performance

Capacitor apps operate inside the host platform's standard web browser engine (WebView).

- **Main JS Thread**: Keep tasks short to prevent blocking browser rendering cycles (aim for under 16ms per frame).
- **Native Bridge Execution**: Calls to native plugins via `Capacitor` bridge are asynchronous. Always handle them using `async/await` or promise chains to avoid UI pauses.
- **Hardware Acceleration**: Use CSS transitions that rely on `transform` and `opacity` to offload animations to the GPU.

---

# Anti-Patterns

❌ **Hardcoded Pixel Widths**: Do not use absolute pixel values that break on smaller mobile screens. Use Tailwind responsive utilities and flexbox layouts.

❌ **Ignoring Safe Areas**: Designing headers or footers that render underneath the camera notch or system home indicator.

❌ **Heavy Local DOM Storage**: Attempting to store large objects in standard LocalStorage (which can be cleared by the OS when memory is low). Use `@capacitor-community/sqlite` for structured databases and `@capacitor/preferences` for small key-value caches.

❌ **Direct DOM Manipulation**: Bypassing React's virtual DOM to write directly to the document elements.

---

# Production Checklist

- [ ] All code conforms to strict TypeScript compiler options.
- [ ] UI layout and safe areas are verified on both iOS and Android emulators.
- [ ] Safe Area environment variables wrap all header and footer layouts.
- [ ] All animations are hardware-accelerated.
- [ ] ESLint and Prettier check runs pass.

---

# Success Criteria

The Capacitor mobile setup is successful when:
- Mobile apps build cleanly for both iOS and Android with a shared codebase exceeding 95% code reuse.
- WebView render speeds remain stable at 60 FPS on mid-tier test devices.
- Developers can configure and spin up a new local emulator within 15 minutes of onboarding.
- Standard coding conventions are enforced automatically via CI linting gates.

---

# Future Evolution

Version 2.0 will include:
- Native swift/kotlin custom plugin development guidelines.
- Continuous deployment integration for asset sync scripts.
- Memory leak analysis and performance profiles inside mobile WebViews.

---

# Document Status

**Document:** NES-400 — Capacitor Mobile Standards
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-401 — Capacitor Architecture**
