---
document_id: NES-613
title: HIPAA Compliance
subtitle: Enterprise HIPAA Security Rule, PHI Protection & Encryption Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Healthcare Platforms Group
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-612 ISO 27001 Compliance
next_document: NES-614 GDPR Compliance
---

# NES-613 — HIPAA Compliance

> **"Patient privacy requires absolute data protection. We secure Protected Health Information (PHI) at rest, in transit, and across all analytical layers."**

---

# Executive Summary

NeelStack's healthcare platforms (e.g. DhruvaOS) process prescriptions, diagnostic reports, and patient files.

These datasets contain **Protected Health Information (PHI)** and are subject to the **Health Insurance Portability and Accountability Act (HIPAA)**.

A compromise of PHI leads to federal penalties, loss of license, and breach of patient trust.

This standard defines the technical safeguards, encryption requirements, access policies, and transmission security required for HIPAA compliance.

---

# Purpose

This standard defines:

- Protected Health Information (PHI) Classification
- Technical Safeguards (Access Control, Encryption)
- PHI Transmission Security
- Business Associate Agreements (BAA)
- Breach Notification Rule

---

# PHI Data Classification

All systems must classify data fields to identify PHI.

- **Definition**: PHI includes any health status, provision of healthcare, or payment data that can be linked to an individual (e.g. name, date of birth, medical record number, email, biometric data).
- **Rule**: Isolating PHI from application logs is mandatory. PHI fields must be scrubbed automatically (NES-517) before log shipping.

---

# Technical Safeguards & Access

To restrict PHI access to authorized staff only:

- **Audit Controls**: Log all queries, reads, updates, and deletes of PHI data.
- **Unique Identification**: Anonymous or shared user accounts are strictly prohibited on healthcare databases. All reads must link to a verified SSO user.
- **Automatic Logoff**: Configure mobile and web applications to log out users automatically after 15 minutes of inactivity.

---

# Transmission & Encryption Security

Secure data transfers and storage using verified encryption standards:

- **At Rest**: Encrypt all PHI datastores using KMS Customer Managed Keys. Plaintext PHI on database disks or backup volumes is a critical violation.
- **In Transit**: Enforce TLS 1.3 for all endpoints. Block TLS 1.0 and 1.1.
- **Envelope Encryption**: Column-level encryption (NES-606) is required for database tables containing patient SSNs or medical records.

---

# Business Associate Agreements (BAA)

We must ensure that all third-party vendors and cloud providers who process PHI sign a **Business Associate Agreement (BAA)**.

- **AWS BAA**: Enforce the AWS Business Associate Addendum. Only deploy healthcare workloads on AWS services that are marked as "HIPAA Eligible."
- **SaaS Vendors**: Verify that external services (e.g. email dispatchers, SMS gateways, telemetry services) have active BAAs before routing any customer PHI through their APIs.

---

# Breach Notification Rule

In the event of an unauthorized disclosure or data breach involving PHI:

- **Incident Timeline**: The Operations Team must notify the Compliance Officer immediately.
- **Notification**: If the breach affects 500 or more individuals, we must notify the Department of Health and Human Services (HHS) and prominent media outlets within **60 days** of discovery, and notify all affected individuals without delay.

---

# Anti-Patterns

❌ **Hardcoded PHI inside Dev Environments**: Exporting active production patient databases to local machines for debugging. Developers must use mock datasets for local testing.

❌ **Exposing PHI in Push Payloads**: Sending patient names or diagnostic details directly in push notification payloads.

❌ **Omitting Audit Logs on Reads**: Tracking database "Write" actions while ignoring "Read" actions. Under HIPAA, auditing who *viewed* a patient record is just as critical as auditing who changed it.

---

# Production Checklist

- [ ] Active BAA agreements exist for AWS and all third-party dependencies.
- [ ] Database access logging (Audit trail) is operational.
- [ ] Automated logoff timer (15 minutes) is active.
- [ ] S3 buckets containing PHI use KMS encryption with Object Lock active.
- [ ] Developers have completed HIPAA security awareness training.

---

# Success Criteria

The HIPAA Compliance implementation is successful when:
- 100% of PHI data is encrypted at rest and in transit.
- Audit logs capture all read and write queries targeting patient databases.
- HHS audits confirm compliance with the HIPAA Security and Privacy rules.

---

# Document Status

**Document:** NES-613 — HIPAA Compliance
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-614 — GDPR Compliance**
