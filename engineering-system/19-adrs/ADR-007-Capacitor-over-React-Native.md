# ADR-007 — Capacitor over React Native

## Status
**Accepted** — In effect as of 2026-07-04

## Context
DhruvaOS requires native iOS and Android mobile interfaces for parents and staff. We previously had a legacy React Native codebase (`apps/mobile-rn`) which was frozen due to high maintenance costs, package version mismatch issues during React/Expo upgrades, and duplicate CSS layout work between our Next.js web console and the native mobile portal.

We evaluated:
1. **React Native (Legacy)**: High-performance native components but requires separate styled layout styling.
2. **Capacitor 7**: Wraps standard React + Vite HTML/CSS web clients into native webviews with full access to native iOS/Android device APIs.

## Decision
We chose **Capacitor 7** because it allows complete visual reuse of our TailwindCSS design system. We can develop our mobile client as a standard web application (`apps/mobile`), bundle it with Capacitor, and compile high-performance native binaries.

## Consequences
- **Code Reuse**: We achieve 100% layout and UI component reuse between web and mobile client views.
- **Maintenance**: No React Native bridges or native iOS/Android build configurations to debug.
