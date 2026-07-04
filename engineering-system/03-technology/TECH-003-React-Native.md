---
document_id: TECH-003
title: React Native + Expo Standard
subtitle: React Native with Expo SDK is the approved mobile framework for all NeelStack mobile apps
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Mobile Platform Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-002 Next.js
next_document: TECH-004 FastAPI
---

# TECH-003 — React Native + Expo Standard

---

## Approved Version

**React Native** (latest stable) + **Expo SDK 52+** with **Expo Router v4**

## Core Stack

| Package | Purpose | Required |
|---|---|---|
| `expo-router` | File-based navigation | ✅ |
| `zustand` | State management | ✅ |
| `nativewind` v4 | Tailwind CSS for native | ✅ |
| `@tanstack/react-query` | Server state | ✅ |
| `expo-secure-store` | Encrypted local storage | ✅ |
| `@sentry/react-native` | Crash reporting | ✅ |
| `msw` | API mocking in tests | ✅ |
| `detox` | E2E testing | ✅ |

## Project Structure

```
app/
├── (auth)/          # Auth screens
├── (tabs)/          # Tab navigation
└── _layout.tsx      # Root layout
components/
├── ui/              # Design system components
└── features/        # Feature components
stores/              # Zustand stores
hooks/               # Custom hooks
services/            # API service layer
```

## Release Process

- iOS: TestFlight → App Store (via EAS)
- Android: Internal testing → Google Play (via EAS)
- OTA updates: Expo Updates for JS-only changes

## Related Standards

- NES-400 — React Native Standards
- NES-401 — Expo Architecture
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
