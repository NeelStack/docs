---
document_id: NES-1206
title: CMS
subtitle: Enterprise Headless Content Management System (CMS) Reference Architecture Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Enterprise Platforms Board
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-1205 Marketplace
next_document: NES-1207 E-commerce
---

# NES-1206 — CMS

> **"Content delivery requires edge caching. This reference blueprint details our headless CMS API routing, CDN caches, and asset storage pipelines."**

---

# Executive Summary

To operate a reliable Content Management System (CMS) that serves pages, blogs, and asset libraries to millions of users, we must optimize content delivery and edge caching.

This document establishes the official **NeelStack Headless CMS Reference Architecture** blueprint.

It defines our API delivery layers, CDN configurations, asset storage pipelines (S3), and content rendering frameworks.

---

# Purpose

This standard defines:

- Unified Headless CMS Reference Architecture Map
- Headless API Delivery and Routing
- Global Edge Caching (CDN Configuration)
- Asset Storage and Optimization (S3)

---

# CMS Reference Architecture Map

The CMS Reference Architecture separates page authors from content delivery:

```text
               Public Ingress (Client App Integrations, HTTPS)
                               │
                               ▼
        Cloudflare Edge (Brotli compression, Page Caches)
                               │
                               ▼
        Headless API Layer (FastAPI / GraphQL, Read-Replicas)
                               │
                               ▼
        Storage Zone (PostgreSQL for content metadata)
         ├── Amazon S3 (Asset storage, images, PDFs)
         └── Redis Cache (API query schema caches)
```

---

# Headless API Delivery Standards

Decouple editing from presentation:

- **Headless Model**: Expose content metadata through scoped REST or GraphQL APIs, allowing client frontends (React/Next.js) to render pages dynamically.
- **Read Replicas**: Route API requests to database read replicas to protect primary databases from read query loads.

---

# Global Edge Caching

Optimize page response times:

- **Cache-Control**: Enforce aggressive caching headers on CMS content APIs:
  ```text
  Cache-Control: public, max-age=86400, stale-while-revalidate=3600
  ```
- **Purge Hooks**: Configure webhooks to trigger Cloudflare cache invalidation automatically when authors publish updates.

---

# Asset Storage & Optimization

- **S3 Storage**: Store images, video assets, and documents inside secure S3 buckets.
- **Edge Formatting**: Route assets through Cloudflare Image Optimization pipelines to convert formats (e.g. to WebP/AVIF) and adjust sizing based on client request headers.

---

# Anti-Patterns

❌ **Monolithic Rendering**: Rendering complete HTML pages on database servers during every client request.

❌ **Exposing Authoring Dashboards**: Exposing editing dashboards on public subdomains without IP whitelists or SSO.

❌ **No Cache Headers**: Serving CMS API responses without cache-control headers, forcing every request to query database disks.

---

# Production Checklist

- [ ] CMS API endpoints expose REST/GraphQL paths.
- [ ] Edge caching (Cloudflare) is active with automatic purge webhooks.
- [ ] Media assets reside in KMS encrypted S3 buckets.
- [ ] Ingress APIs have active rate limits.
- [ ] Authoring portals use Entra ID SSO.

---

# Success Criteria

The CMS Reference Architecture is successful when:
- Content pages render in less than 1.5 seconds globally.
- CDN cache hit ratios for content APIs exceed 90%.
- Database CPU loads remain low during traffic spikes.

---

# Document Status

**Document:** NES-1206 — CMS
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1207 — E-commerce**
