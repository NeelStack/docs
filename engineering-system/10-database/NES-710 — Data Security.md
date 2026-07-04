---
document_id: NES-710
title: Data Security
subtitle: Enterprise Data Classifications, Masking & Access Policy Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Data Governance & Security Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-709 Data Governance
next_document: NES-711 Lineage
---

# NES-710 — Data Security

> **"Data protection must match classification value. We enforce granular access policies, dynamic data masking, and absolute audit loops."**

---

# Executive Summary

Analytical data platforms aggregate databases from multiple source systems, creating a high-value target for attackers.

If developers, business analysts, or third-party tools have unrestricted access to raw warehouse tables, patient health files (PHI) or personal details (PII) can be leaked.

This standard establishes the data classification guidelines, column and row-level security parameters, dynamic data masking rules, and access retention policies for NeelStack data warehouses.

---

# Purpose

This standard defines:

- Data Classification Matrix (Public, Internal, PII, PHI)
- Row-Level Security (RLS) & Column-Level Security (CLS)
- Dynamic Data Masking Configurations
- Analytical Queries Auditing
- Data Retention and Archiving Rules

---

# Data Classification Matrix

All datastores and tables must categorize their fields according to the following classification hierarchy:

| Level | Definition | Security Controls |
|---|---|---|
| **Public** | Marketing files, documentation. | No restrictions. |
| **Internal** | Non-sensitive business metrics. | Access limited to SSO profiles. |
| **PII (Personal)** | Names, phone numbers, addresses. | Masking by default, encryption at rest (NES-606). |
| **PHI (Health)** | Patient diagnosis, prescription logs. | STRICT isolation (NES-613), signed BAA, full audit logs. |

---

# Granular Security Policies (RLS & CLS)

Manage database queries using the principle of least privilege:

- **Column-Level Security (CLS)**: Block access to columns containing sensitive identifiers (like SSNs or emails) for non-administrative roles.
- **Row-Level Security (RLS)**: Enforce partition filtering to ensure tenant analysts or developers can only execute queries against tables filtered by their respective tenant IDs (NES-706).

---

# Dynamic Data Masking

For queries that require access to tables containing PII for business analytics:

- **Masking Rules**: Database engines must apply dynamic masking to obscure sensitive characters before returning queries:
  - *Email*: Mask as `j***@neelstack.com`.
  - *Credit Card*: Mask as `xxxx-xxxx-xxxx-1234`.
  - *Social Security Number*: Mask completely.

```sql
-- Snowflake dynamic masking policy configuration
CREATE OR REPLACE MASKING POLICY email_mask AS (val string) RETURNS string ->
  CASE
    WHEN CURRENT_ROLE() IN ('SECURITY_ADMIN') THEN val
    ELSE REGEXP_REPLACE(val, '.+@', '***@')
  END;
```

---

# Query Audit Logging

Every read operation against classified data must generate audit trails.

- **Audited Queries**: Log the query string, user SSO identifier, timestamp, and number of returned rows for every select statement executed against PII/PHI databases.
- **Anomaly Detection**: Trigger alerts if a user account executes a query that exports more than 10,000 PII records, indicating potential data extraction attacks.

---

# Data Retention & Erasure

Maintain data hygiene limits in the warehouse:

- **Retention Rules**: Prune analytics databases after 3 years unless business regulations require longer archiving times.
- **Right to be Forgotten**: Enforce automated scripts to clean and erase user profiles from warehouse analytics schemas within 30 days of deletion requests (NES-614).

---

# Anti-Patterns

❌ **Universal Admin Database Roles**: Granting developers shared database administrator roles (`db_owner`) for general query work.

❌ **Saving Cleartext SSNs in Views**: Creating database view tables that expose unmasked sensitive identifiers to reporting tools.

❌ **Excluding Log Audits**: Failing to log query requests, leaving security teams blind to which users have viewed customer records.

---

# Production Checklist

- [ ] Data classifications are mapped in DataHub catalogs.
- [ ] Row-Level and Column-Level security policies are active.
- [ ] Dynamic data masking is active on all PII columns.
- [ ] Database query logs are shipped to the central SIEM.
- [ ] Warehouse users authenticate exclusively via Entra ID SSO.

---

# Success Criteria

The Data Security program is successful when:
- Unauthorized database query roles receive masked characters instead of plaintext PII values.
- Database access audit logs capture all queries targeting transactional databases.
- Analytical data stores maintain complete isolation boundaries between customer tenants.

---

# Document Status

**Document:** NES-710 — Data Security
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-711 — Lineage**
