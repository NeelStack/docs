---
document_id: TECH-003
title: Capacitor Standard
subtitle: React + Vite + Capacitor is the approved mobile framework for all NeelStack mobile apps
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Mobile Platform Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-002 Next.js
next_document: TECH-004 FastAPI
---

# TECH-003 — Capacitor Standard

---

## Approved Version

**React 19** + **Vite 6** + **Capacitor 7** with **React Router Dom v7**

## Core Stack

| Package | Purpose | Required |
|---|---|---|
| `@capacitor/core` | Core runtime container | ✅ |
| `@capacitor/android` | Android platform support | ✅ |
| `@capacitor/ios` | iOS platform support | ✅ |
| `@capacitor-community/sqlite` | Offline SQL storage | ✅ |
| `@capacitor-firebase/messaging` | Firebase push notifications | ✅ |
| `react-router-dom` | Browser-based routing | ✅ |
| `zustand` | State management | ✅ |
| `tailwindcss` v3 | Styling layout system | ✅ |
| `@tanstack/react-query` | Server state fetching | ✅ |
| `@capacitor/preferences` | Key-value settings storage | ✅ |
| `vitest` | Unit and integration testing | ✅ |

## Project Structure

```
src/
├── components/      # UI design system components
├── features/        # Feature domain folders (e.g. attendance)
├── hooks/           # Custom React hooks
├── services/        # Backend API clients
├── stores/          # Zustand global state stores
└── main.tsx         # App bootstrap entry
android/             # Android studio native project folder
ios/                 # Xcode native project folder
capacitor.config.js  # Capacitor bridge configurations
vite.config.js       # Vite build configurations
```

## Release Process

- iOS: Compile native workspace → Xcode archive → TestFlight / App Store
- Android: Compile native workspace → Android Studio sign → Google Play
- Live Updates: Over-the-air JS/CSS asset updates via `@capawesome/capacitor-live-update`

## Related Standards

- NES-400 — Capacitor Mobile Standards
- NES-401 — Capacitor Architecture
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
