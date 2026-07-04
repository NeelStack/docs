---
document_id: NES-1415
title: Disaster Recovery Topology
subtitle: Enterprise Disaster Recovery & Multi-Region Failover Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Operations Team
review_cycle: Every 6 Months
document_type: Reference Implementation
parent_document: NES-1414 — Security Trust Boundaries.md
next_document: NES-1416 — CI-CD Pipelines.md
---

# NES-1415 — Disaster Recovery Topology

> **"Failover must be proven and continuous. This reference blueprint details our multi-region replication, health checkers, and DNS failover topologies."**

---

# Executive Summary

To operate a highly available platform that can survive complete regional cloud outages or data center failures, we must enforce a structured disaster recovery strategy.

This document establishes the official **NeelStack Disaster Recovery Topology** blueprint.

It defines our multi-region configurations, database replication streams, DNS health checks, and active-passive failover routes.

---

# Purpose

This standard defines:

- Unified Multi-Region Disaster Recovery Topology Map
- Active-Passive vs. Active-Active Hosting Setup
- RDS Database Replication Streams (Read Replicas)
- Cloudflare DNS Failover and Health Checks

---

# Disaster Recovery Topology Map

The Disaster Recovery Topology organizes resources across primary and secondary regions:

```text
               Public Client Traffic (subdomain.neelstack.com)
                               │
                               ▼
        Cloudflare Edge (DNS Failover / Health monitors)
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼ (Health check PASS)                           ▼ (Primary FAIL - Route traffic)
  Primary region (AWS us-east-1)                 Secondary region (AWS us-west-2)
  ├── Active EKS Cluster                         ├── Standby EKS Cluster (Scale 0)
  └── Primary RDS Instance ─── (Cross-Region) ──►└── RDS Read Replica (Promote to Write)
```

---

# Multi-Region Deployment Modes

To manage costs while meeting recovery targets:

- **Active-Passive (Warm Standby)**: We run an active cluster in the primary region (`us-east-1`) and keep a standby, scale-to-zero cluster in the secondary region (`us-west-2`).
- **Target RTO / RPO**:
  - **Recovery Time Objective (RTO)**: **< 15 minutes** (to promote RDS replicas and scale compute).
  - **Recovery Point Objective (RPO)**: **< 1 minute** (maximum data loss from replication lag).

---

# RDS Cross-Region Replication

Secure database data replication:

- **Replication Stream**: Configure asynchronous cross-region replication for production PostgreSQL databases from the primary to the standby region.
- **Standby Promotion**: When a primary regional outage is confirmed, SREs trigger automated scripts (or manual checks) to promote the secondary replica to a writeable instance.

---

# Cloudflare DNS Failover & Health Checks

- **Health Monitors**: Cloudflare probes the primary region ingress health endpoints (`/healthz`) every 15 seconds.
- **Failover Routing**: If primary endpoint probes fail for 3 consecutive intervals, Cloudflare dynamically updates DNS CNAME records to route user traffic to the secondary region ALB.

---

# Anti-Patterns

❌ **Manual DNS Swaps during Outages**: Managing DNS updates manually inside domain consoles during outages, which increases downtime.

❌ **Shared Databases for Multi-Region Compute**: Connecting primary and secondary clusters to a single regional database, creating a single point of failure.

❌ **Omitting Failover Tests**: Failing to test disaster recovery failovers regularly, leading to failure discovery during live outages.

---

# Production Checklist

- [ ] Multi-region VPC configurations are active.
- [ ] Database cross-region replication is running.
- [ ] Cloudflare health monitors are active.
- [ ] Failover scripts are verified.
- [ ] Backup restore procedures are audited monthly.

---

# Success Criteria

The Disaster Recovery Topology implementation is successful when:
- Regional failover completes within the 15-minute RTO target.
- Data replication lag to the secondary region remains under 1 minute.
- DNS health checks update routing automatically during tests.

---

# Document Status

**Document:** NES-1415 — Disaster Recovery Topology
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1416 — CI-CD Pipelines.md**
