---
document_id: NES-1200
title: SaaS Reference Architecture
subtitle: Enterprise Multi-Tenant SaaS Platform Reference Architecture
version: 1.0.0
status: Draft
classification: Internal
owner: Architecture Review Board
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-1107 Platform Roadmap
next_document: NES-1201 Healthcare Platform
---

# NES-1200 — SaaS Reference Architecture

> **"SaaS scalability requires strict tenant isolation. This reference blueprint details our multi-tenant database partitioning, routing rules, and compute structures."**

---

# Executive Summary

To operate a reliable Software-as-a-Service (SaaS) platform, we must maintain a unified architectural model across all customer tenants.

This document establishes the official **NeelStack Multi-Tenant SaaS Reference Architecture** blueprint.

It defines our tenant isolation boundaries, multi-tenant database partitioning (Postgres schemas), routing configurations, and compute namespace isolation.

---

# Purpose

This standard defines:

- Unified Multi-Tenant SaaS Architecture Map
- Tenant Data Isolation (Shared DB with RLS vs. Isolated Schema)
- Tenant Ingress Routing and Subdomains
- Tenant Compute Isolation Boundaries

---

# SaaS Reference Architecture Map

The NeelStack SaaS Reference Architecture divides resource layers into tenant-isolated zones:

```text
               Public Ingress (Client Subdomains: *.neelstack.com)
                               │
                               ▼
        Cloudflare Edge (Tenant Routing & Custom Domains)
                               │
                               ▼
        EKS Cluster Boundary (Namespace Isolation per Tier)
         ├── Free Tier Namespace (Shared compute resources)
         ├── Enterprise Namespace (Dedicated pod resources)
         └── Istio Ingress (Tenant header validations)
                               │
                               ▼
        Multi-Tenant Database Zone (AWS RDS PostgreSQL)
         ├── Shared DB with Row-Level Security (RLS) for Free/Standard
         └── Dedicated Database Instances for Enterprise clients
```

---

# Tenant Data Isolation Standards

We enforce data isolation based on customer subscription tiers:

- **Shared Database (Logical Isolation)**: Standard tiers share database tables. Queries must enforce Row-Level Security (RLS) dynamically using `tenant_id` session keys.
- **Dedicated Database (Physical Isolation)**: Enterprise clients are provisioned with dedicated database instances to prevent "noisy neighbor" resource starvation.

---

# Tenant Ingress Routing & Subdomains

- **Subdomain Routing**: Assign each tenant a unique subdomain (e.g. `client.neelstack.com`).
- **Dynamic Configuration**: Cloudflare routes traffic dynamically based on tenant subdomain headers, verifying tenant status before forwarding requests to target ingress ALBs.

---

# Anti-Patterns

❌ **Hardcoded Database Tenant Queries**: Constructing SQL strings without tenant filtering, risking cross-tenant data leaks.

❌ **Shared Connection Pools for Enterprise**: Forcing enterprise tenants to share database connection pools with free-tier users, risking connection exhaustion during load spikes.

❌ **Exposing Tenant Admin Routes**: Leaving administrative routes unprotected by IP whitelists, exposing tenant consoles.

---

# Production Checklist

- [ ] SaaS tenant isolation policies are active.
- [ ] Database schemas support RLS configurations.
- [ ] Dynamic subdomain routing is operational.
- [ ] Tenant access logs are routed to the central SIEM.
- [ ] Client status dashboards track tenant resource footprints.

---

# Success Criteria

The SaaS Reference Architecture is successful when:
- Tenant data is completely isolated logically or physically.
- Outages or load spikes in one tenant do not affect neighboring tenants.
- System metrics demonstrate sub-second response times for all tiers.

---

# Document Status

**Document:** NES-1200 — SaaS Reference Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1201 — Healthcare Platform**
