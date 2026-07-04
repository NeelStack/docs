---
document_id: NES-511
title: CDN
subtitle: Enterprise Content Delivery Network, Cache Headers & Assets Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-510 Multi-Cloud (Azure & GCP)
next_document: NES-512 Networking
---

# NES-511 — CDN

> **"Static assets belong at the edge. We distribute images, script bundles, and documents globally using CDNs with optimized caching headers."**

---

# Executive Summary

Loading website bundles, script files, design assets, and large media files directly from origin servers slows down page render speeds, exhausts origin web server connections, and generates high egress data transfer costs.

We mandate the routing of all public static assets through a Content Delivery Network (CDN) to ensure local, sub-second asset delivery.

This standard defines cache control headers, invalidation strategies, and asset optimization rules.

---

# Purpose

This standard defines:

- CDN Architecture (Cloudflare CDN / CloudFront)
- HTTP Cache Control Headers
- Automated Cache Invalidation Strategies
- Asset Optimization (Compression, Format conversion)
- Dynamic Edge Routing Policies

---

# CDN Architecture

We utilize a dual CDN tier depending on the asset category:

- **Web Static Assets (JS, CSS, HTML)**: Distributed globally using **Cloudflare CDN Edge Nodes**.
- **Media and Document Storage (S3 Uploads)**: Distributed using **Amazon CloudFront** integrated with Origin Access Control (OAC) to secure the S3 source buckets.

---

# HTTP Cache Control Headers

To optimize local browser caching and edge node caching, web servers must return explicit `Cache-Control` headers.

### Standard Cache-Control Rules:

- **Immutable Assets (Hash-compiled JS, CSS, fonts)**: Cache aggressively on both browser and edge nodes.
  ```text
  Cache-Control: public, max-age=31536000, immutable
  ```
- **Dynamic Documents (HTML files, JSON configurations)**: Force validation on every connection, preventing stale render states.
  ```text
  Cache-Control: no-cache, no-store, must-revalidate
  ```
- **User Private Uploads (Protected PDFs, certificates)**: Do not cache on public CDNs or shared nodes.
  ```text
  Cache-Control: private, no-store
  ```

---

# Cache Invalidation Strategies

When deploying updates, stale files must be cleared instantly.

- **Cache-Busting (Filename hashing)**: Build pipelines must include unique content hashes in filenames (e.g. `main.d83a74e.js`). This allows old files to age out naturally while new updates load instantly.
- **API Invalidation**: For dynamic caches, utilize tag-based purging (`Cache-Tag` header) to purge specific resource groups via API calls without wiping the entire global CDN cache.

---

# Asset Optimization at the Edge

CDNs must be configured to compress and optimize payloads on-the-fly:

- **Compression**: Enforce **Brotli** compression (or Gzip as fallback) for all text assets (HTML, JS, CSS, JSON).
- **Format Conversion**: Convert images dynamically to modern, optimized web formats (e.g. **WebP** or **AVIF**) based on browser compatibility headers.

---

# Anti-Patterns

❌ **Hardcoded URL Domains**: Embedding absolute URLs (like `https://s3.amazonaws.com/my-bucket/image.png`) inside component files. This bypasses the CDN entirely and exposes origin buckets. Use CDN alias domains (`https://cdn.neelstack.com/image.png`).

❌ **Cache-Control Defaults**: Leaving default web server configurations active, which often omit cache-control headers or apply short temporary caching to static JS bundles.

❌ **Manual Cache Purging**: Purging the entire CDN cache manually via the cloud console on every deployment, which causes massive origin traffic spikes.

---

# Production Checklist

- [ ] Private assets are served with `Cache-Control: private, no-store`.
- [ ] Compression settings (Brotli) are active on CDN controllers.
- [ ] Origin Access Control (OAC) is active on Amazon CloudFront to block direct S3 bypass.
- [ ] Filename hashing is configured for all built frontend assets.
- [ ] Edge invalidation tags are verified as functional.

---

# Success Criteria

The CDN configuration is successful when:
- Average page load time is reduced by more than 50% compared to origin server direct access.
- Origin servers experience zero traffic spikes during static asset reloads.
- Egress network transfer billing costs are reduced.

---

# Document Status

**Document:** NES-511 — CDN
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-512 — Networking**
