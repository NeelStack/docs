---
document_id: TECH-002
title: Next.js Standard
subtitle: Next.js is the approved web frontend framework for all NeelStack products
version: 1.0.0
status: L3 - Enterprise
classification: Internal
owner: Frontend Platform Team
review_cycle: Every 6 Months
document_type: Technology Standard
parent_document: TECH-001 Technology Stack
next_document: TECH-003 React Native
---

# TECH-002 — Next.js Standard

---

## Approved Version

**Next.js 15.x** (App Router) with **React 19.x**

Pin exact version in `package.json`. Update only after ARB review.

## Required Configuration

```ts
// next.config.ts
const config: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,
  images: { formats: ['image/avif', 'image/webp'] },
  experimental: { typedRoutes: true },
}
```

## Router Standard

All new projects use the **App Router** (`/app` directory). Pages Router is legacy — no new projects use it.

## Project Structure

```
app/
├── (auth)/         # Auth group routes
├── (dashboard)/    # Dashboard group routes
├── api/            # API routes
├── globals.css
└── layout.tsx
components/
├── ui/             # Primitive UI components
├── features/       # Feature-specific components
└── layouts/        # Layout components
lib/
├── api/            # API client helpers
├── hooks/          # Custom React hooks
└── utils/          # Utility functions
```

## Performance Requirements

- Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
- All pages scored ≥ 90 on Lighthouse
- Dynamic imports for heavy components

## Related Standards

- NES-300 — Frontend Engineering Standards
- NES-311 — Frontend Performance Standards
- TECH-001 — Technology Stack

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-07-04 | Initial publication |
