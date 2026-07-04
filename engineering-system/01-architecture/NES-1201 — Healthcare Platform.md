---
document_id: NES-1201
title: Healthcare Platform
subtitle: Enterprise Healthcare Platform Reference Architecture (DhruvaOS)
version: 1.0.0
status: Draft
classification: Internal
owner: Healthcare Platforms Group
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-1200 SaaS Reference Architecture
next_document: NES-1202 ERP
---

# NES-1201 — Healthcare Platform

> **"DhruvaOS is defined by patient safety and security boundaries. This reference blueprint details our HIPAA compliance, PHI isolation, and audit trail configurations."**

---

# Executive Summary

To operate a reliable healthcare platform (DhruvaOS) that processes clinical records, patient files, and diagnostic data, we must enforce a strict security model.

This document establishes the official **DhruvaOS Healthcare Platform Reference Architecture** blueprint.

It defines our Protected Health Information (PHI) isolation borders, end-to-end data encryption configurations, access control matrices, and audit logging pathways.

---

# Purpose

This standard defines:

- Unified Healthcare Platform Architecture Map
- Protected Health Information (PHI) Isolation Boundaries
- End-to-End Encryption Configuration (TLS 1.3, Envelope)
- Immutable Audit Trail Pipelines

---

# DhruvaOS Reference Architecture Map

The DhruvaOS Reference Architecture divides systems into secure compliance zones:

```text
               Public Ingress (Client Subdomains, TLS 1.3 Only)
                               │
                               ▼
             AWS ALB Ingress (HTTPS, Strict TLS Ciphers)
                               │
                               ▼
        Hardened EKS Compute VPC (Private Subnets)
         ├── App Containers (runAsNonRoot, readOnlyRootFS)
         └── Secrets CSI Driver (In-memory tmpfs mount)
                               │
                               ▼
        Isolated Data Zone (AWS RDS Postgres, Multi-AZ)
         ├── Transparent Data Encryption (TDE) active
         └── Column-level Envelope Encryption active
                               │
                               ▼
        Immutable Log Zone (S3 Object Lock Compliance Mode)
```

---

# PHI Data Isolation Standards

Protect patient privacy across storage systems:

- **Network Isolation**: Databases and cache instances processing PHI must reside in isolated subnets with zero route tables leading to internet gateways.
- **Log Masking**: Configure ingestion pipelines (Vector) to strip PII and PHI from debug logs before shipping them to analytical databases (NES-517).

---

# End-to-End Encryption

Enforce strict cryptography across all nodes:

- **In Transit**: Minimum supported protocol is **TLS 1.3** for all internal and external communication.
- **At Rest**: Enforce SSE-KMS storage encryption on all databases and backup files.
- **Envelope Encryption**: Implement column-level envelope encryption (NES-606) for patient identifiers (e.g. social security numbers, medical records).

---

# Immutable Audit Logging

Every transaction targeting patient databases must compile an immutable log:

- **Audit Capture**: Write logs detailing the user identity, client IP, timestamp, and query targets.
- **WORM Target**: Write log outputs to S3 buckets configured in **Compliance Mode (WORM)**, preventing file deletion or modification by any administrator (NES-610).

---

# Anti-Patterns

❌ **Plaintext PHI in Log Streams**: Printing patient names, phone numbers, or prescriptions inside standard console logs.

❌ **Exposing Diagnostic APIs to Public Networks**: Exposing internal patient database APIs directly on public endpoints without strict mTLS boundaries.

❌ **Shared Dev-Prod Datastores**: Connecting developer test instances to databases containing real patient files.

---

# Production Checklist

- [ ] DhruvaOS systems conform to the Healthcare Reference Architecture map.
- [ ] Columns containing PHI use active Envelope Encryption.
- [ ] S3 Object Lock is active on the audit log bucket.
- [ ] AWS BAA agreement is signed and active.
- [ ] Container security rules are active on EKS nodes.

---

# Success Criteria

The Healthcare Reference Architecture is successful when:
- 100% of PHI data is encrypted at rest and in transit.
- Audit logs capture all read and write queries targeting patient databases.
- HIPAA and SOC2 compliance audits confirm zero active security findings.

---

# Document Status

**Document:** NES-1201 — Healthcare Platform
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-1202 — ERP**
