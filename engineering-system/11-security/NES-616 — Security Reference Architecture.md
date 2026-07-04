---
document_id: NES-616
title: Security Reference Architecture
subtitle: Enterprise Security Reference Architecture, Trust Boundaries & Encryption Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-615 Security Operations (SecOps)
next_document: NES-700 Data Platform Standards
---

# NES-616 — Security Reference Architecture

> **"A secure system is mapped and understood. This reference blueprint details the trust zones, data encryption keys, and network security boundaries."**

---

# Executive Summary

To protect enterprise applications and comply with strict regulations, we must maintain a unified, auditable security layout across our cloud networks.

This document establishes the official **NeelStack Security Reference Architecture** blueprint.

It defines our trust boundaries, encryption key configurations, audit logging streams, dynamic secret drivers, and network vulnerability scanning endpoints.

---

# Purpose

This standard defines:

- Unified Security Reference Architecture Map
- Ingress and Egress Trust Boundaries
- Encryption Key Layout (KMS, CMK, Envelope)
- Security Verification Checklist

---

# Security Reference Architecture Map

The NeelStack Security Reference Architecture divides the network and data layers into secure trust zones:

```text
               Public Internet (Untrusted Zone)
                              │
  Boundary 1: TLS 1.3 ────────┼──────────────────────────────────
                              ▼
        Edge Proxy Zone (Cloudflare WAF, DDoS Mitigation)
                              │
  Boundary 2: Proxy IP Only ──┼──────────────────────────────────
                              ▼
        Ingress Load Balancer (AWS ALB, Public Subnets)
                              │
  Boundary 3: VPC mTLS ───────┼──────────────────────────────────
                              ▼
        Private Compute Zone (EKS Compute Nodes, Private Subnets)
         ├── App Containers (runAsNonRoot, readOnlyRootFS)
         ├── Secrets CSI Driver (In-memory tmpfs mount)
         └── Falco Agent (Host kernel sys-call monitoring)
                              │
  Boundary 4: IAM Auth ───────┼──────────────────────────────────
                              ▼
        Isolated Data Zone (RDS PostgreSQL, KMS Encrypted)
         ├── Transparent Data Encryption (TDE) active
         └── Column-level Envelope Encryption active
```

---

# Ingress & Egress Boundaries

Our security borders block unauthorized lateral movement:

- **Ingress Boundary Control**: The EKS private network only accepts connections coming from the AWS ALB security group. Direct node port access is disabled globally.
- **Egress Boundary Control**: Pod outbound connections to external endpoints are routed through the Istio Egress Gateway, which blocks connection requests to un-whitelisted domain destinations.

---

# Cryptographic Key Mapping

To secure data at rest (TDE) and columns containing PII (Envelope Encryption):

- **KMS Master Key (CMK)**: Managed securely in AWS KMS. Enforce annual key rotation.
- **Data Encryption Key (DEK)**: Generated locally inside the application memory using AES-256-GCM. Plaintext DEK is discarded from memory immediately after usage.
- **Encrypted DEK**: Stored alongside the encrypted data records inside the isolated database tables.

---

# Telemetry & Compliance Log Routing

Security events must follow an absolute, non-modifiable shipping pipeline:

- **Audit Logs**: Generated inside containers, formatted as JSON, and scraped by FluentBit.
- **Storage**: Vector routes audit events to an S3 bucket configured in **Compliance Mode (WORM)**, preventing log erasure or modification.
- **Analysis**: Logs are scraped by OpenSearch Security Analytics to identify and alert on potential security breaches.

---

# Anti-Patterns

❌ **Flat Security Groups**: Creating a single security group for EKS nodes, RDS databases, and load balancers, allowing any service to communicate with databases.

❌ **Omitting KMS Key Policies**: Leaving the default KMS key policy open to all accounts, bypassing least-privilege key constraints.

❌ **Writable Container Root Filesystems**: Permitting containers to run with write access to root directories, allowing hackers to download and install persistent malware files.

---

# Production Checklist

- [ ] Network boundaries match the Security Reference Architecture map.
- [ ] Columns containing patient PHI or personal PII use Envelope Encryption.
- [ ] S3 Object Lock is active on the audit log bucket.
- [ ] Container security rules (runAsNonRoot, readOnlyRootFilesystem) are active.
- [ ] AWS GuardDuty reports zero active alerts.

---

# Success Criteria

The Security Reference Architecture is successful when:
- Internal databases are unreachable from any external connection outside the VPC.
- Outbound traffic from private nodes is consolidated through Egress gateways for monitoring.
- Audit logs provide an absolute, non-modifiable record of system actions.

---

# Document Status

**Document:** NES-616 — Security Reference Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-700 Data Platform Standards**
