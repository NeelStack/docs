---
document_id: NES-416
title: Mobile Reference Architecture
subtitle: Enterprise Mobile Directory Layout & Shared Code Architecture
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Board
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-415 Mobile AI
next_document: NES-500 Platform Engineering Standards
---

# NES-416 — Mobile Reference Architecture

> **"A clean architecture structures execution paths predictably. This reference blueprint governs the folder layout, module boundaries, and dependency patterns for all mobile codebases."**

---

# Executive Summary

To scale mobile development and maintain an enterprise-grade codebase, we enforce a structured directory layout.

This standard establishes the official **NeelStack Capacitor Reference Architecture**, defining module boundaries, service configurations, and monorepo code sharing constraints.

---

# Purpose

This standard defines:

- Directory Layout Blueprint for Vite + Capacitor
- Module responsibility boundaries
- Code sharing standards in Monorepos

---

# Directory Layout Blueprint

All mobile client applications must align with the following structural layout:

```text
/
├── android/                  # Android Studio native platform project
├── ios/                      # Xcode native platform project
├── public/                   # Static public assets (icons, splash)
├── src/                      # Single Page Application source code
│   ├── components/           # Reusable UI component wrappers
│   │   ├── ui/               # Shared primitives (buttons, modals)
│   │   └── common/           # Shared views (headers, tabs layout)
│   │
│   ├── features/             # Feature modules
│   │   └── document/         # Document feature scope
│   │       ├── components/   # Feature-specific UI
│   │       ├── hooks/        # Feature queries (TanStack hooks)
│   │       ├── store/        # Feature store (Zustand client store)
│   │       └── services/     # Feature HTTP requests
│   │
│   ├── routes/               # Navigation routing configurations
│   │   └── index.ts          # React Router v7 routes map
│   │
│   ├── services/             # Global native bridges and services
│   │   ├── api.ts            # Network client setup
│   │   ├── secureStore.ts    # Secure Storage wrapper
│   │   └── telemetry.ts      # Analytics tracker
│   │
│   ├── styles/               # CSS inputs
│   │   └── index.css         # Tailwind directives and safe-area utilities
│   │
│   ├── main.tsx              # App initialization entry point
│   └── App.tsx               # Root component wrapping router providers
│
├── capacitor.config.ts       # Capacitor bridge config
├── vite.config.ts            # Vite compiler configuration
├── package.json              # App dependency declaration
└── tailwind.config.js        # Tailwind CSS config
```

---

# Module Responsibility Boundaries

- **Routes (`src/routes`)**: Focus strictly on path configurations and layouts. Do not place business calculations or direct API call functions inside path declarations.
- **Features (`src/features`)**: Group code by feature domains. Features must not import files directly from other features (shared logic must reside in global components or services).
- **Services (`src/services`)**: Enforce standard integrations with native plugins and custom API instances.

---

# Code Sharing (Web Console vs. Mobile Client)

In a monorepo workspace (NES-102), because both our Next.js admin console and our Capacitor mobile client compile to standard HTML5 / React, we can share extensive sections of the UI code:

- **Highly Shareable**:
  - **Types**: Type definitions and payload validation (Zod schemas).
  - **Business Logic**: Hooks, helpers, utility modules, and Zustand client store parameters.
  - **UI Styling**: Tailwind CSS theme tokens.
  - **Component Primitives**: Unstyled logic components, form components, or standard buttons/cards that use standard Tailwind styling tags.
- **Not Shareable**:
  - **Navigation**: Next.js uses server-optimized file routing, while the mobile client uses SPA client routing (`react-router-dom`).
  - **Native Features**: Plugins referencing specific device libraries (e.g. camera, biometrics) must be wrapped in platform checks if used in files shared with Next.js web applications.

---

# Anti-Patterns

❌ **Importing React Native styles**: Copying code with React Native stylesheet elements (`StyleSheet.create`) or React Native tags (`View`, `Text`), which will crash the Vite build.

❌ **Direct Native Calls inside Shared Elements**: Placing Capacitor plugins directly inside components shared with the Next.js web project without checks, causing crashes when running in web browsers.

---

# Production Checklist

- [ ] Directory layout conforms to the Vite + Capacitor blueprint.
- [ ] Shared components do not import platform-specific dependencies without fallback checks.
- [ ] Tailwind configurations mirror the monorepo design system parameters.

---

# Success Criteria

The Reference Architecture is successful when:
- Shared components render identically on both Next.js console pages and Capacitor WebView emulators.
- The project builds cleanly with zero circular dependencies or package conflicts.
- Codebase reuse across mobile web views and web consoles exceeds 80%.

---

# Document Status

**Document:** NES-416 — Mobile Reference Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-500 Platform Engineering Standards**
