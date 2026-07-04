---
document_id: NES-416
title: Mobile Reference Architecture
subtitle: Enterprise Mobile Directory Layout, Shared Code & Reference Architecture
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

To scale mobile applications across multiple development teams and maintain an enterprise-grade codebase, we must enforce a structured, consistent directory layout.

This document establishes the official **NeelStack Mobile Reference Architecture** blueprint, outlining module boundaries, utility paths, configuration standards, and code-sharing constraints.

---

# Purpose

This standard defines:

- Directory Layout Blueprint
- Module Responsibility Boundaries
- Dependency Rules
- Code Sharing Conventions (Web vs. Mobile)
- Reference Architecture Checklist

---

# Directory Layout Blueprint

All mobile codebases must align with the following directory structure:

```text
/
├── app/                      # Expo Router File-Based Navigation
│   ├── _layout.tsx           # Global Providers and Layout Configuration
│   ├── index.tsx             # Entry Point (Splash Screen or Redirects)
│   ├── (auth)/               # Authentication Route Group
│   └── (app)/                # Authenticated Application Screens
│
├── src/                      # Source Code Container
│   ├── components/           # UI Elements
│   │   ├── ui/               # Reusable UI Primitives (Button, Input, Card)
│   │   └── common/           # Shared Common Components (Header, Loader)
│   │
│   ├── features/             # Feature-Driven Modules
│   │   ├── document/         # Document Feature Domain
│   │   │   ├── components/   # Feature-Specific UI
│   │   │   ├── hooks/        # Feature Hooks (e.g. useDocumentQuery)
│   │   │   ├── store/        # Feature Client Store (e.g. useDocStore)
│   │   │   └── services/     # Feature API Communications
│   │   └── profile/          # Profile Feature Domain
│   │
│   ├── services/             # Global Platform Services
│   │   ├── api.ts            # Network client configuration
│   │   ├── secureStore.ts    # Secure Storage Interface
│   │   └── telemetry.ts      # Global Event Logging
│   │
│   ├── styles/               # Global Styles and Style Tokens
│   │   └── global.css        # NativeWind Stylesheet Import
│   │
│   └── utils/                # Pure helper functions
│
├── assets/                   # Static Resources (Fonts, Images, Icons)
├── plugins/                  # Local Expo Config Plugins
├── tailwind.config.js        # NativeWind configuration
├── app.json                  # Static Expo Configuration
├── app.config.ts             # Dynamic Expo Configuration
└── eas.json                  # EAS Build/Submit profiles
```

---

# Module Responsibility Boundaries

To maintain clean architecture boundaries:

- **Screens (`/app`)**: Keep layouts thin. They must focus strictly on routing, parameter parsing, and wrapping UI views in layout structure. Avoid declaring API calls directly inside screen components.
- **Features (`src/features`)**: Group components, hooks, stores, and types by feature domains. Features must not import components or hooks directly from other features (shared logic must reside in `src/components/ui` or `src/services`).
- **Services (`src/services`)**: Define connections to external systems (HTTP request client, push managers, telemetry, secure local storage).

---

# Code Sharing (Web vs. Mobile)

When sharing code within a monorepo setup (NES-102) between our Next.js frontend and React Native mobile applications:

- **Shareable**: Domain types (TypeScript interfaces), API payload schemas, validation schemas (Zod), helper functions (`utils`), and translation dictionaries.
- **Not Shareable**: UI components, navigation logic, and styling. The web uses HTML/Next.js tags while mobile uses React Native native layouts (views, texts). Trying to combine these into single multi-platform UI files introduces high maintenance costs and compromises quality.

---

# Architecture Verification Rules

We verify code patterns automatically using custom ESLint rules to prevent architectural drift:

- **Constraint 1**: `src/components/ui` must not import anything from `src/features` (prevents circular dependencies).
- **Constraint 2**: Features must communicate with external APIs via `src/services/api` configuration (standardizes request headers, tokens, and telemetry).

---

# Anti-Patterns

❌ **Direct Native Calls in Components**: Importing native components directly into screens. Wrap them in clean interfaces under `src/components/ui` to support cross-platform stubbing during tests.

❌ **Monolithic Files**: Creating files containing database setup, API controllers, helper calculations, and UI styling in a single screen module.

❌ **Loose App configurations**: Pushing raw credentials, keys, or passwords straight into `app.json`. Use environment variables dynamically injected via `app.config.ts`.

---

# Production Checklist

- [ ] Directory layout matches the Mobile Reference Architecture blueprint.
- [ ] No file exceeds the maximum line size limitations (NES-400).
- [ ] Shared configurations (eslint, tailwind) match monorepo requirements.
- [ ] Code sharing boundaries are validated.
- [ ] Documentation updated.

---

# Success Criteria

The Reference Architecture is successful when:
- Developers can locate any component, hook, or API client interface instantly based on the directory layout.
- The project compiles cleanly from scratch without circular import failures.
- Changes to shared types or API schemas propagate automatically across both web and mobile workspaces.

---

# Document Status

**Document:** NES-416 — Mobile Reference Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-500 Platform Engineering Standards**
