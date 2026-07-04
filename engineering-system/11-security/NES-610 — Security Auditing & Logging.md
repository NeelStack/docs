---
document_id: NES-610
title: Security Auditing & Logging
subtitle: Enterprise Immutable Audit Trails & SIEM Integration Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Platform Security Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-609 Security Compliance Framework
next_document: NES-611 SOC2 Compliance
---

# NES-610 — Security Auditing & Logging

> **"Logs are the legal record of system operations. We generate immutable audit logs, prevent deletion, and analyze threats using SIEM dashboards."**

---

# Executive Summary

To investigate security breaches, satisfy regulatory compliance (SOC2, HIPAA, GDPR), and trace data modifications, we must maintain an absolute audit trail.

Standard application debug logs (INFO/WARN) are insufficient because they are mutable, ephemeral, and frequently deleted.

We mandate the isolation of security and operational event logs into a separate, immutable logging pipeline.

This standard defines the log schema, security event classifications, S3 Object Lock configuration, and SIEM integration rules.

---

# Purpose

This standard defines:

- Security Audit Event Classifications
- Immutable Logging Architecture (S3 Object Lock)
- SIEM Integration and Analysis (OpenSearch Security Analytics)
- Security Log Schemas and Required Fields
- Rotation, Deletion, and Archival constraints

---

# Audit Event Classifications

The following categories of events must trigger an immediate audit log entry:

- **Authentication**: Successful logins, failed authentication attempts, MFA resets.
- **Authorization**: API access privilege changes, directory group modification, database access role creation.
- **Data Modification (Write/Delete)**: Updates or deletes to user profiles, document deletions, database schema migrations.
- **Secrets Access**: Secrets Manager fetches, dynamic database token requests (NES-514).
- **Network Boundaries**: Ingress/Egress proxy block actions, configuration drift detection.

---

# Immutable Log Architecture

Audit logs must be protected from deletion or tampering, even by administrators with compromised root keys.

- **Storage Target**: Route all audit events to dedicated **Amazon S3 Object Lock** buckets configured in **Compliance Mode**.
- **WORM Enforced**: Once written, compliance mode blocks log modification or deletion by any IAM user (including the AWS root user) for the retention period.
- **Digital Signatures**: Sign audit files cryptographically at creation time (using HMAC or KMS keys) to detect modifications.

```text
  Application Log Event
            │
            ▼
   Vector Shipping Agent (JSON)
            │
            ▼
  Amazon S3 (Object Lock bucket)
   - Compliance Mode Active
   - KMS SSE Encrypted
   - Cryptographic Signatures
```

---

# Security Event Schema

Audit logs must follow a strict, non-customizable schema to support automated SIEM parsing:

```json
{
  "timestamp": "2026-07-04T12:00:00.000Z",
  "event_id": "aud_123456",
  "event_type": "AUTH_FAILED",
  "actor": {
    "id": "usr_987",
    "email": "user@neelstack.com",
    "ip_address": "198.51.100.42"
  },
  "resource": {
    "id": "tenant_123",
    "type": "TENANT_CONFIG"
  },
  "action": "UPDATE_PERMISSION",
  "status": "DENIED",
  "reason": "Insufficient RBAC role"
}
```

---

# SIEM Integration (Security Analytics)

We stream audit logs from S3 buckets to our central Security Information and Event Management (SIEM) dashboard using **OpenSearch Security Analytics**.

- **Detection Rules**: Configure SIEM filters to trigger immediate Slack or PagerDuty alerts on suspicious event sequences, such as:
  - More than 5 failed logins within 1 minute from the same IP address.
  - A secret accessed by an EKS pod from outside the allowed namespace list.
  - Deletion of multiple database tables in a single session.

---

# Anti-Patterns

❌ **Mutable Audit Logs**: Storing security audit logs on standard EBS volumes or writeable databases where an attacker with root database access can delete logs to hide their trail.

❌ **Exposing PII in Audits**: Including patient health details, personal identifiers, or login passwords inside audit log properties.

❌ **Omitting Actor IPs**: Logging changes like "User profile updated" without capturing the source IP address or device identifier.

---

# Production Checklist

- [ ] S3 audit log bucket is configured in Compliance Mode.
- [ ] Audit event schema is validated.
- [ ] KMS SSE encryption is active.
- [ ] Weekly audit log signature validations run automatically.
- [ ] SIEM alert rules are active and verified.

---

# Success Criteria

The Security Auditing and Logging program is successful when:
- 100% of defined security events are written to the immutable vault.
- Modifying or deleting audit logs is blocked.
- Security incidents can be traced back to the source IP address and user account.

---

# Document Status

**Document:** NES-610 — Security Auditing & Logging
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-611 — SOC2 Compliance**
