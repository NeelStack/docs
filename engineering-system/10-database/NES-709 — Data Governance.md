---
document_id: NES-709
title: Data Governance
subtitle: Enterprise Data Catalog, Metadata Discovery & Quality Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Data Governance Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-708 Feature Store
next_document: NES-710 Data Security
---

# NES-709 — Data Governance

> **"Data without description is dark data. We catalog all data assets, define ownership, and assert quality boundaries continuously."**

---

# Executive Summary

As databases and data lakes expand, identifying where specific fields are stored, who owns them, and whether they are accurate becomes highly complex.

Untracked datasets lead to redundant engineering efforts, compliance violations, and bad analytical decisions based on outdated fields.

We mandate the enforcement of **Data Governance** across all NeelStack database platforms.

This standard establishes our metadata discovery protocols (**Amundsen / DataHub**), business glossary mappings, data ownership definitions, and automated data quality checks (**Great Expectations**).

---

# Purpose

This standard defines:

- Metadata Catalog and Discovery (DataHub / Amundsen)
- Data Ownership and Domain Roles
- Business Glossary Standards
- Data Quality Framework (Great Expectations)
- Data Quality SLA Rules

---

# Data Discovery & Metadata Catalog

We centralize database descriptions inside the **Metadata Catalog** (powered by **DataHub**).

- **Catalog Scoping**: The platform automatically crawls schema tables weekly (RDS PostgreSQL, Snowflake warehouses, S3 Glue Catalogs).
- **Searchability**: All tables, schemas, and columns must be searchable via the DataHub dashboard.
- **Descriptions**: Table schema definitions in dbt or database migrations must include description comments:

```sql
COMMENT ON COLUMN students.registration_date IS 'The UTC timestamp when the student profile was registered.';
```

---

# Data Ownership & Domain Roles

Every database table, warehouse schema, and ingestion pipeline must have an assigned owner:

- **Data Owner**: Typically a Product Manager or business lead responsible for defining the fields, permissions boundaries, and business rules.
- **Data Steward**: An engineer responsible for the pipeline execution, schema migrations, and operational uptime.

---

# Data Quality Framework

Never assume source database fields are formatted correctly. We standardize on **Great Expectations** to enforce data assertions.

- **Check Assertions**: Define automated checks for data quality parameter checks:
  - Columns must have zero null values where required.
  - Value ranges must remain within physical limits (e.g. `age` between 1 and 120).
  - Schema structures must match the expected configuration.

```python
# Reference Great Expectations check definition
import great_expectations as ge

df = ge.read_parquet("s3://neelstack-data-lake/raw/students/data.parquet")
df.expect_column_values_to_not_be_null("student_id")
df.expect_column_min_to_be_between("age", min_value=3, max_value=100)
```

---

# Data Quality SLAs

Configure pipeline runs to report quality metrics:

- **Pipeline Interrupts**: If a critical data quality check fails during ingestion transformations, the pipeline must abort write steps, preventing invalid data from entering the warehouse.
- **Warning Logs**: Non-critical failures (like minor missing tags) log warn messages to Slack.

---

# Anti-Patterns

❌ **Orphaned Databases**: Spawning development databases or S3 buckets without registering them in the centralized metadata catalog.

❌ **Excluding Table Comments**: Writing database schemas without table or column level comments, leaving description metrics undocumented.

❌ **Silent Data Corruption**: Allowing pipeline scripts to process and write null values in key columns without throwing errors or halting executions.

---

# Production Checklist

- [ ] DataHub crawler has active connections to all database engines.
- [ ] Database columns include description comments.
- [ ] Great Expectations checks are integrated with Airflow DAGs.
- [ ] Table ownership mappings are declared in the catalog.
- [ ] Ingestion pipeline SLA thresholds are verified.

---

# Success Criteria

The Data Governance implementation is successful when:
- Developers can search and locate any data field description in the catalog in less than 30 seconds.
- Invalid data schemas are blocked automatically in the ingestion phase.
- Ownership mappings are active for all production tables.

---

# Document Status

**Document:** NES-709 — Data Governance
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-710 — Data Security**
