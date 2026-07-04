---
document_id: NES-614
title: GDPR Compliance
subtitle: Enterprise GDPR Compliance, Privacy by Design & Data Erasure Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Governance & Compliance Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-613 HIPAA Compliance
next_document: NES-615 Security Operations (SecOps)
---

# NES-614 — GDPR Compliance

> **"Privacy is a fundamental right. We implement Privacy by Design, enforce data minimization, and build automated systems to handle user data erasure requests."**

---

# Executive Summary

Applications handling personal data of European Union (EU) citizens must conform to the **General Data Protection Regulation (GDPR)**.

Violations of GDPR rules can result in fines up to €20 million or 4% of global annual turnover, alongside loss of user trust.

This standard establishes our Privacy by Design principles, personal data definitions, user consent guidelines, data residency rules, and automated erasure protocols (Right to be Forgotten).

---

# Purpose

This standard defines:

- Personal Data Classification under GDPR
- Privacy by Design & Data Minimization
- Consent Management (Cookies, ATT)
- Right to Erasure (Right to be Forgotten) Implementation
- Data Residency and Sovereign Cloud Routing

---

# Personal Data Classification

We classify user data using GDPR definitions:

- **Personal Data**: Any information relating to an identified or identifiable natural person (e.g. name, email, IP address, device location, purchase history).
- **Special Category Data**: Highly sensitive personal data (e.g., biometric data, health records, racial origin) requiring explicit consent and high-security encryption controls.

---

# Privacy by Design & Data Minimization

Engineering teams must design architectures that minimize personal data collection:

- **Minimization**: Do not collect user data "in case we need it later." Only request parameters that are strictly necessary to deliver the active feature.
- **Pseudonymization**: Replace identifying parameters with random hashes or keys at the service boundary.
- **Anonymization**: For statistical calculations, ensure data is completely anonymized and cannot be reversed or linked back to a user profile.

---

# Right to Erasure (Right to be Forgotten)

Under GDPR Article 17, users have the right to request the complete deletion of their personal data.

- **Automated Deletion**: The platform team provides an automated cleanup script. When a user profile is flagged as "Deleted," the script must run across all active database tables and S3 file stores to erase matching data records within **30 days**.
- **Log Cleaning**: Ensure that backup restoration processes do not reload deleted user records back into active databases.

```text
  User Deletion Request
           │
           ▼
 Flag User in DB as "Deleted"
           │
           ▼
 Trigger Cleanup Job (Async)
 ├── Erase DB Rows (Postgres)
 ├── Delete Files (S3)
 └── Purge Analytics Indexes
           │
           ▼
 30-Day Completion SLA met
```

---

# Data Residency & Sovereign Cloud

EU citizen data must reside inside EU boundaries.

- **Data Residency**: Configure AWS VPC and RDS instances for EU clients in European regions (e.g., `eu-west-1` Dublin).
- **Sovereign Cloud Routing**: Route requests to local datastores based on client geolocation checks at the Edge proxy (Cloudflare).

---

# Anti-Patterns

❌ **Hard-Deleting with Orphaned Records**: Deleting a user row from the main database while leaving their personal email inside logs, cache stores, or backup databases.

❌ **Pre-checked Consent Boxes**: Using pre-checked tick boxes for marketing tracking on signup pages. Consent must be freely given, specific, and informed.

❌ **Exposing IP Addresses in General Logs**: Storing plaintext client IP addresses in standard debug logs. Treat IPs as personal data and mask them.

---

# Production Checklist

- [ ] Privacy Policy documents detail what personal data is gathered.
- [ ] Automated user data erasure scripts are verified.
- [ ] Cookie consent banners require opt-in before loading tracking scripts.
- [ ] Data residency routing is active for EU tenants.
- [ ] Employees have completed GDPR compliance training.

---

# Success Criteria

The GDPR Compliance program is successful when:
- User data deletion requests are processed, confirmed, and verified across all systems in under 30 days.
- Cookie scanners confirm that no marketing cookie is loaded before user opt-in approval.
- Data privacy audits show zero unencrypted personal data stored in public files.

---

# Document Status

**Document:** NES-614 — GDPR Compliance
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-615 — Security Operations (SecOps)**
