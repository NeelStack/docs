---
document_id: ADR-003
title: React Native + Expo for Mobile Development
status: Superseded by ADR-007
date: 2026-07-04
deciders: CTO, Chief Architect, Mobile Lead
consulted: Mobile Engineering Team
informed: All Engineering
---

# ADR-003 — React Native + Expo for Mobile Development

## Status

**Superseded** — Superseded by [ADR-007 — Capacitor over React Native](file:///d:/poc/docs/engineering-system/19-adrs/ADR-007-Capacitor-over-React-Native.md) on 2026-07-04.

## Context

NeelStack products (EduOS, DhruvaOS, NaukariMitra) require native mobile apps for iOS and Android. Requirements:
- Single codebase for iOS and Android
- Native performance for educational video and offline scenarios
- Code sharing with React web frontend
- OTA (Over-the-Air) updates for JS changes
- Strong India market device support

## Decision

**We will use React Native with Expo SDK** as the mobile development framework.

Specifically:
- **Expo SDK 52+** with **Expo Router v4** for file-based navigation
- **EAS Build** for CI/CD builds
- **EAS Update** for OTA updates

## Consequences

### Positive
- 90%+ code sharing with React web (types, API clients, business logic)
- OTA updates allow instant bug fixes without App Store review
- EAS Build eliminates need for macOS build machines
- Strong support for India's device diversity (low-RAM device optimizations)
- Native modules available via Expo plugins

### Negative
- Not suitable for extremely performance-sensitive apps (games, AR)
- React Native bridge adds some overhead vs fully native
- Expo SDK update cycle requires periodic upgrades

## Alternatives Considered

| Alternative | Rejected Reason |
|---|---|
| Flutter | Dart language — no code sharing with React web stack |
| Native iOS/Android | 2× development cost, 2× teams required |
| Ionic | Web-based, poor native performance |
| Capacitor | Web-based, same performance concerns as Ionic |

## Related Standards

- NES-400 — React Native Standards
- NES-401 — Expo Architecture
- TECH-003 — React Native + Expo Standard
