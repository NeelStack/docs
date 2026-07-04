---
document_id: NES-508
title: Cloudflare
subtitle: Enterprise Edge Networking, DNS, WAF & Cloudflare Standards
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-507 Helm
next_document: NES-509 AWS
---

# NES-508 — Cloudflare

> **"Security and speed begin at the edge. We route all public traffic through Cloudflare to secure DNS, enforce WAF rules, and optimize edge caching."**

---

# Executive Summary

Every application exposed to the public internet is vulnerable to DDoS attacks, malicious scans, credential stuffing, and data injection.

Additionally, users require fast responses regardless of their physical distance from origin servers.

NeelStack standardizes on **Cloudflare** as our edge networking layer.

This standard defines DNS configurations, Web Application Firewall (WAF) policies, SSL configuration rules, and edge caching strategies.

---

# Purpose

This standard defines:

- DNS Management and Routing
- Web Application Firewall (WAF) Rules
- SSL/TLS Encryption Levels
- Edge Caching and Optimization
- DDoS Mitigation and Rate Limiting

---

# DNS Management & Routing

All domain records (e.g. `*.neelstack.com`, `portal.neelstack.com`) must be managed inside Cloudflare.

- **Proxied Status (Orange Cloud)**: Ensure all public HTTP/HTTPS records have the proxy status enabled (represented by the orange cloud in the dashboard). This hides our origin IP addresses and intercepts traffic at the edge.
- **Apex Redirection**: Configure permanent redirects (`301`) from apex domains (`neelstack.com`) to subdomains (`www.neelstack.com`) at the edge using Cloudflare Redirect Rules.

---

# Web Application Firewall (WAF)

Enforce strict edge security filters to drop malicious traffic before it reaches our cloud load balancers.

### Standard WAF Rules:

1. **OWASP Anomaly Score**: Enable the OWASP rule set with sensitivity set to "Medium/High".
2. **IP Access Rules**: Block or challenge traffic coming from high-risk hosting providers or regions that do not serve active customers.
3. **API Protection**: Restrict POST/PUT requests to api endpoints (`/api/*`) by enforcing rate limits per IP address (e.g. max 100 requests per minute).

---

# SSL/TLS Encryption Standard

To prevent intercept attacks and ensure end-to-end encryption:

- **SSL Mode**: Always configure SSL/TLS encryption mode to **Strict (Full)**. This forces Cloudflare to validate the origin server's SSL certificate, preventing MITM attacks.
- **TLS Version**: Minimum supported TLS version is **1.3** (or 1.2 for legacy clients if strictly necessary). Disallow TLS 1.0 and 1.1.
- **HSTS (HTTP Strict Transport Security)**: Enable HSTS to force browsers to connect only via HTTPS.

```text
  Client (HTTPS)
        │
        ▼ (TLS 1.3)
   Cloudflare Edge (WAF/DDoS check)
        │
        ▼ (Full/Strict SSL)
  Origin Load Balancer
```

---

# Edge Caching & Optimization

Reduce origin load by caching static assets globally.

- **Cache Everything Rule**: Apply page rules to cache static layouts (`*.js`, `*.css`, `/assets/*`) at edge nodes with long TTLs (e.g. 7 days).
- **Cache Invalidation**: Configure build pipelines to trigger purge requests (`Purge Cache by Tag`) when releasing new frontend bundles, avoiding stale displays.

---

# Anti-Patterns

❌ **Grey Clouding APIs**: Leaving proxied status disabled (grey cloud) for backend API endpoints, which exposes public IP addresses of our load balancers to DDoS attacks.

❌ **Flexible SSL Settings**: Setting SSL encryption level to "Flexible". This encrypts connection from user to Cloudflare, but sends traffic from Cloudflare to origin in cleartext HTTP.

❌ **Wildcard Cache Bypass**: Failing to configure caching on static assets, forcing every image/script reload to fetch directly from cloud servers, driving up cloud exit costs.

---

# Production Checklist

- [ ] All public domain records are proxied (Orange Clouded).
- [ ] SSL/TLS mode is set to "Full (Strict)".
- [ ] Minimum TLS version is set to 1.3.
- [ ] WAF rules and OWASP scores are active.
- [ ] HSTS is enabled with a minimum duration of 1 year.

---

# Success Criteria

The Cloudflare edge configuration is successful when:
- 100% of origin server IP addresses are hidden from public lookup tools.
- Distributed DDoS attacks are absorbed at the edge without reaching origin servers.
- Static assets have a cache hit ratio exceeding 85% at edge nodes.

---

# Document Status

**Document:** NES-508 — Cloudflare
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-509 — AWS**
