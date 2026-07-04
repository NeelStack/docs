---
document_id: NES-519
title: Disaster Recovery
subtitle: Enterprise RTO/RPO Metrics, Database Replication & Failover Standard
version: 1.0.0
status: Draft
classification: Internal
owner: SRE & Platform Operations Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-518 Incident Response
next_document: NES-520 Platform Reference Architecture
---

# NES-519 — Disaster Recovery

> **"Hope is not a disaster recovery strategy. We design multi-region databases, enforce target recovery metrics, and simulate outages regularly."**

---

# Executive Summary

Disasters can take the form of complete cloud provider region outages, physical datacenter cuts, database corruptions, ransomware locks, or accidental database deletions.

Without a tested Recovery Plan, a disaster can lead to permanent data loss or days of system downtime.

This standard defines the recovery objectives, multi-region database patterns, backup policies, and disaster recovery simulation rules.

---

# Purpose

This standard defines:

- Recovery Time Objective (RTO) & Recovery Point Objective (RPO)
- Multi-Region Database Replication (Active-Passive / Active-Active)
- Automated Failover DNS Routing
- Backup Retention and Encryption Rules
- Disaster Recovery Simulation (Game Days)

---

# Core Recovery Metrics (RTO & RPO)

We define target metrics based on service tier criticality:

- **Recovery Time Objective (RTO)**: The maximum allowed duration of system downtime before restoration (e.g. how fast we must restore service).
- **Recovery Point Objective (RPO)**: The maximum allowed data loss window (e.g. age of files we must restore from backup).

### Target Matrix:

| Tier | Services | Target RTO | Target RPO |
|---|---|---|---|
| **Tier 1 (Critical)** | Authentication, Core Web APIs, Databases. | < 15 Minutes | < 1 Minute |
| **Tier 2 (Major)** | Notification system, Document processing. | < 4 Hours | < 1 Hour |
| **Tier 3 (Minor)** | Internal analytics, Reporting tools. | < 24 Hours | < 24 Hours |

---

# Multi-Region Database Replication

To satisfy Tier 1 target metrics, data must be replicated across separate physical regions:

- **Primary DB (Active)**: Handles active user reads and writes in the main region (e.g. AWS `us-east-1`).
- **Replica DB (Passive)**: Receives async replication changes in the fallback region (e.g. AWS `us-west-2`).
- **Failover**: If the main region goes down, the database manager automatically promotes the replica database to primary write status.

```text
       AWS US-East-1 (Active)
   ┌─────────────────────────────┐
   │  EKS cluster ──► Active RDS │
   └──────────────────────┬──────┘
                          │ (Async Replication)
                          ▼
       AWS US-West-2 (Passive)
   ┌─────────────────────────────┐
   │  EKS cluster ──► Replica RDS│
   └─────────────────────────────┘
```

---

# Automated DNS Failover

When a regional outage occurs, redirect user connections automatically.

- **Standard**: Configure Cloudflare DNS Routing using Health Checks.
- **Mechanism**: Cloudflare monitors the health check endpoint (`/health/live`). If the primary region fails to respond to checks for 3 consecutive minutes, Cloudflare automatically updates the CNAME routing records to point to the fallback load balancer in the passive region.

---

# Backup Security & Retention

Backups must survive ransomware attacks and infrastructure compromises.

- **WORM (Write Once Read Many)**: Store database backups in S3 Object Lock buckets configured in compliance mode to prevent deletion or editing by anyone (even root admins) for the retention period.
- **Encryption**: Enforce KMS-SSE encryption on all backup repositories.
- **Retention**: Keep daily backups for 30 days, weekly backups for 90 days, and yearly snapshots for 7 years.

---

# DR Game Days

A disaster recovery plan is only valid if it has been executed and proven successful under load.

- **Frequency**: SRE and Platform teams must host **Disaster Recovery Game Days** every **6 months**.
- **Execution**: Simulate complete database failure, network drops, or regional shutdowns inside staging/test environments, measuring actual RTO/RPO metrics against target limits.

---

# Anti-Patterns

❌ **Untested Backups**: Taking database snapshots daily but never testing restoration processes. This frequently leads to discovery of corrupt backups during live outages.

❌ **Manual Failover Dependencies**: Requiring manual configuration edits in multiple consoles to update routing during an active incident. Failovers must be automated or executed with a single script trigger.

❌ **Running Backups in the Same AWS Account**: Storing backups in the same AWS account as the active databases. If the AWS account is compromised, the backups are deleted.

---

# Production Checklist

- [ ] Multi-region database replication is verified.
- [ ] DNS failover health checks are configured.
- [ ] S3 object lock is enabled for backup repositories.
- [ ] Target RTO/RPO matrices are documented.
- [ ] Game Day schedule is set and approved.

---

# Success Criteria

The Disaster Recovery program is successful when:
- Regional failover triggers, routes, and restores complete application state in less than 15 minutes.
- Data recovery audits show zero records lost during failover events.
- Game Day simulations verify that SRE operators can execute recovery runbooks without error.

---

# Document Status

**Document:** NES-519 — Disaster Recovery
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-520 — Platform Reference Architecture**
