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

> **"Accelerate mobile development with React Native and Expo. This starter kit provides a production-ready repository configured with Expo Router, NativeWind, Zustand, and MSW."**

---

# Executive Summary

To help developer teams launch new mobile application features quickly while maintaining architectural alignment, performance standards, and security compliance, we provide the **Mobile Starter Kit**.

This starter kit contains a pre-configured template containing file-based routing, style theme tokens, state management caches, offline-first connection handlers, and testing configs.

This document establishes the repository structure, approved tech stack, quick start guide, and verification steps for the Mobile Starter template.

---

# Purpose

This standard defines:

- Mobile Starter Repository Directory Structure
- Pre-Configured Tech Stack
- Quick Start Guide for Developers
- Pre-Integrated Security and CI/CD Gates

---

# Repository Directory Structure

The Mobile Starter repository utilizes a clean React Native directory structure:

```text
mobile-starter/
├── app/                   # Expo Router screens (Tabs, Stacks layout)
├── components/            # Reusable UI component elements
├── hooks/                 # Custom React hooks (TanStack queries)
├── store/                 # Global state stores (Zustand)
├── utils/                 # Utilities and helper modules
├── .github/
│   └── workflows/         # EAS Build and Test workflows
├── app.json               # Expo configurations & plugins
├── tailwind.config.js     # Style theme tokens config
└── README.md
```

---

# Pre-Configured Tech Stack

The template includes our approved technology stack configured for production:

- **Framework**: Expo (SDK 51+), React Native.
- **Routing**: Expo Router (file-based).
- **Styling**: NativeWind (Tailwind CSS v3).
- **State Management**: Zustand (Client), TanStack Query v5 (Server), AsyncStorage.
- **Testing**: Jest, React Native Testing Library, Mock Service Worker (MSW).

---

# Quick Start Guide

Developers can spin up the local development sandbox inside 2 minutes:

1. **Clone Template**: Create a new repository using the Mobile Starter template.
2. **Environment Variables**: Copy `.env.example` to `.env` in the root folder.
3. **Install Dependencies**: Run package installations:
   ```bash
   npm install
   ```
4. **Start Development Server**: Launch Expo Go development server:
   ```bash
   npm start
   ```
5. **Run on Simulators**: Press `i` to launch on iOS Simulator, or `a` for Android Emulator.

---

# Pre-Integrated Security & CI/CD Gates

The template includes built-in security features to prevent vulnerability leakage:

- **Secure Store Integration**: Out-of-the-box configuration for `expo-secure-store` to encrypt tokens.
- **Network Security Configuration**: SSL Pinning parameters pre-configured inside app profiles.
- **EAS Configs**: Ready-to-run configurations for EAS Build and OTA updates pipelines.

---

# Anti-Patterns

❌ **Direct State Mutability**: Modifying state attributes directly inside views instead of executing Zustand actions.

❌ **Exposing Access Tokens in Plaintext**: Storing user tokens in cleartext AsyncStorage volumes instead of using `expo-secure-store` API structures.

❌ **Omitting Component Tests**: Adding screens without writing Jest rendering checks.

---

# Production Checklist

- [ ] Template repository clone completes cleanly.
- [ ] Local Expo development server runs successfully.
- [ ] App renders properly in simulators.
- [ ] CI pipeline linting and unit tests pass.
- [ ] EAS configs are mapped.

---

# Success Criteria

The Mobile Starter template is successful when:
- Teams can spin up a new mobile screen in less than 5 minutes.
- The template codebase passes local Jest unit checks with zero failures.
- Render speeds maintain 60 FPS in simulator performance tests.

---

# Document Status

**Document:** NES-1305 — Mobile Starter
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1306 — Admin Starter**
