---
document_id: NES-1305
title: Mobile Starter
subtitle: Enterprise Mobile Starter Kit & Template Specification
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Engineering Team
review_cycle: Every 6 Months
document_type: Starter Kit
parent_document: NES-1304 Healthcare Starter
next_document: NES-1306 Admin Starter
---

# NES-1305 — Mobile Starter

> **"Accelerate mobile development with React, Vite, and Capacitor. This starter kit provides a production-ready repository configured with React Router v7, Tailwind CSS, Zustand, and Vitest."**

---

# Executive Summary

To help development teams launch new mobile features quickly while maintaining architectural alignment, performance, and security compliance, we provide the **Mobile Starter Kit**.

This starter kit contains a pre-configured Vite + Capacitor template featuring single-page routing, global state stores, local security plugin wrappers, and unit testing environments.

---

# Purpose

This standard defines:

- Mobile Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The Mobile Starter repository uses a clean web directory structure compiled into native platforms:

```text
mobile-starter/
├── android/               # Android Studio native platform project
├── ios/                   # Xcode native platform project
├── public/                # Static public assets (icons, splash)
├── src/                   # React Single Page Application container
│   ├── components/        # Reusable UI component wrappers
│   ├── features/          # Feature domains modules
│   ├── routes/            # React Router v7 configurations
│   ├── services/          # API clients and Capacitor native bridges
│   ├── stores/            # Zustand global state stores
│   └── main.tsx           # Application entry point
├── .github/
│   └── workflows/         # Build and Test workflows
├── capacitor.config.ts    # Capacitor config
├── vite.config.ts         # Vite bundler configuration
├── tailwind.config.js     # Tailwind CSS config
└── README.md
```

---

# Pre-Configured Tech Stack

The template includes our approved technology stack configured for production:

- **Framework**: React 19 + Vite 6 + Capacitor 7.
- **Routing**: React Router Dom v7.
- **Styling**: Tailwind CSS v3 + safe area utility classes.
- **State Management**: Zustand (Client), TanStack Query v5 (Server), `@capacitor/preferences` persistence.
- **Testing**: Vitest, React Testing Library, Mock Service Worker (MSW).

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the Mobile Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` in the root folder.
3. **Install Dependencies**: Run package installations:
   ```bash
   npm install
   ```
4. **Compile Assets**: Build the web package:
   ```bash
   npm run build
   ```
5. **Sync Platforms**: Copy build files to native containers:
   ```bash
   npx cap sync
   ```
6. **Run on Simulators**: Compile and boot on iOS or Android:
   ```bash
   npx cap run ios
   # or
   npx cap run android
   ```

---

# Pre-Integrated Security & CI/CD Gates

The template includes built-in security features to prevent vulnerability leakage:

- **Secure Storage Integration**: Out-of-the-box configuration for `@capacitor-community/secure-storage` to encrypt tokens.
- **Network Security Configuration**: SSL Pinning parameters pre-configured inside native profiles.
- **Vite Bundle Obfuscation**: JavaScript bundle obfuscator activated for production compilations.

---

# Anti-Patterns

❌ **Direct State Mutability**: Modifying state attributes directly inside views instead of executing Zustand actions.

❌ **Exposing Access Tokens in Plaintext**: Storing user tokens in cleartext Preferences volumes instead of using secure storage wrappers.

❌ **Omitting Component Tests**: Adding screens without writing Vitest rendering checks.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local web build runs and syncs to platforms successfully.
- [ ] App renders properly in simulators.
- [ ] CI pipeline linting and unit tests pass.

---

# Success Criteria

The Mobile Starter template is successful when:
- Teams can spin up a new mobile screen in less than 5 minutes.
- The template codebase passes local Vitest unit checks with zero failures.
- Render speeds maintain 60 FPS in simulator performance tests.

---

# Document Status

**Document:** NES-1305 — Mobile Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1306 — Admin Starter**
