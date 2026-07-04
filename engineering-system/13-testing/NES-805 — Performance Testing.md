---
document_id: NES-805
title: Performance Testing
subtitle: Enterprise Client-Side Performance, Page Speed & Bundle Budget Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Quality Assurance Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-804 E2E Testing
next_document: NES-806 Load Testing
---

# NES-805 — Performance Testing

> **"Slow interfaces degrade customer experience. We enforce rendering budgets, audit bundle sizes, and verify client-side performance on every build."**

---

# Executive Summary

Slow-rendering web layouts and bloated mobile applications cause user drop-off and negatively affect search engine rankings (SEO).

If performance is evaluated only manually on high-speed developer workstations, issues like memory leaks or bloated script bundles will reach production undetected.

We mandate automated **Performance Testing** gates across all NeelStack client-side applications.

This standard establishes our rendering speed metrics (Core Web Vitals), bundle size budget targets, and profiling configurations.

---

# Purpose

This standard defines:

- Core Web Vitals targets
- Automated Page Auditing (Lighthouse CI)
- Frontend Bundle Size Budgets
- Mobile Performance Profiling
- CI/CD Performance Gates

---

# Core Web Vitals Targets

All web applications must satisfy target thresholds for Google's **Core Web Vitals**:

| Metric | Description | Target Threshold |
|---|---|---|
| **LCP** (Largest Contentful Paint) | Measures loading performance (main content load). | **< 2.5 Seconds** |
| **INP** (Interaction to Next Paint) | Measures interface responsiveness. | **< 200 Milliseconds** |
| **CLS** (Cumulative Layout Shift) | Measures visual stability (unexpected shifts). | **< 0.1** |

---

# Page Speed Audits (Lighthouse CI)

Automate page performance analysis inside pull request validation checks:

- **Lighthouse CI (LHCI)**: Execute LHCI checks against built staging application URLs.
- **CI Gates**: Set LHCI configurations to block PR merges if performance audit scores drop below **90/100** points across core page routes.

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "first-contentful-paint": ["warn", {"maxNumericValue": 2000}]
      }
    }
  }
}
```

---

# Bundle Size Budgets

Exceeding Javascript payload limits slows down parsing and rendering speeds on lower-end mobile devices.

- **Bundle Analyzer**: Run webpack or vite bundle analyzers during compilation.
- **Budget Thresholds**: Define strict size limits:
  - **Initial JS Bundle**: Maximum **200KB** (gzipped).
  - **Individual Lazy Loaded Chunk**: Maximum **100KB** (gzipped).
- **Rule**: Build tasks must terminate with errors if built assets exceed budget ceilings (enforced using tools like `bundlesize` or `lighthouse`).

---

# Mobile Performance Auditing

To optimize mobile resource footprints (iOS/Android):

- **Hermes Metrics**: Profile Javascript execution memory using the Hermes engine logs (NES-410).
- **Frame Rate Target**: Maintain rendering performance at a stable **60 FPS** during transition animations.

---

# Anti-Patterns

❌ **Omitting Image Dimensions**: Laying out images without specifying width and height parameters, causing high visual page shift (CLS) as resources load.

❌ **Monolithic Imports**: Importing large third-party modules (e.g. `lodash` or `moment.js`) globally instead of tree-shaking or using lightweight alternatives.

❌ **Excluding Low-Performance Networks**: Evaluating page loading speeds exclusively on local, high-speed networks, masking performance issues on slower connections.

---

# Production Checklist

- [ ] Core Web Vitals conform to defined thresholds.
- [ ] Lighthouse CI assertions are active in the build pipeline.
- [ ] JS bundle size budgets are enforced.
- [ ] Large images are optimized and lazy-loaded.
- [ ] Memory allocation profiling runs verify zero leaks.

---

# Success Criteria

The Performance Testing program is successful when:
- Average LCP metrics remain under 2.5 seconds on mobile connections in production.
- Core Web Vitals reports show zero active CLS warning flags.
- CI pipelines catch and block bundle budget overruns prior to compilation.

---

# Document Status

**Document:** NES-805 — Performance Testing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-806 — Load Testing**
