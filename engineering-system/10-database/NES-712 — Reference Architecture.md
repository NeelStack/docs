---
document_id: NES-712
title: Reference Architecture
subtitle: Enterprise Data Engineering Reference Architecture Blueprint
version: 1.0.0
status: Draft
classification: Internal
owner: Data Engineering Team
review_cycle: Every 6 Months
document_type: Reference Architecture
parent_document: NES-711 Lineage
next_document: NES-800 QA Principles
---

# NES-712 — Reference Architecture

> **"A structured data flow guarantees system reliability. This reference blueprint details our unified data ingestion, storage, and transformation pipelines."**

---

# Executive Summary

To maintain operational consistency across all educational, healthcare, and SaaS systems, we must enforce a single, repeatable architecture design for all data processes.

This document establishes the official **NeelStack Data Engineering Reference Architecture** blueprint.

It defines our ingestion boundaries, storage layout hierarchies, automated transformation systems (dbt), governance integrations, and security enforcement zones.

---

# Purpose

This standard defines:

- Unified Data Engineering Reference Architecture Map
- Ingestion and Storage Layer Details
- Data Quality and Transformation Sequences
- Telemetry and Audit Configurations

---

# Data Engineering Reference Architecture Map

The Data Engineering Reference Architecture defines five stages of data processing:

```text
  [ App Databases ] (Postgres)  ──► [ Debezium CDC ]
                                          │
                                          ▼ (Parquet Files)
  [ Ingestion Ingress Zone ] ──► [ S3 Raw Ingest Bucket ]
                                          │
                                          ▼ (Incremental Loads)
  [ Data Lakehouse Zone ] ──► [ Apache Iceberg Metadata ]
                               │      ├── Glue Data Catalog
                               │      └── AWS Athena Engine
                               │
                               ▼ (dbt compile)
  [ Data Warehouse Zone ] ──► [ Snowflake Schema Layers ]
                               ├── Staging Views (stg_)
                               ├── Intermediate Tables (int_)
                               └── Marts Star Schemas (fct_ / dim_)
                                          │
       ┌──────────────────────────────────┴──────────────────────────────────┐
       ▼                                  ▼                                  ▼
  [ Serving Zone ] ──► [ BI Dashboards ]    [ ML Feature Stores ]    [ External API Exports ]
                      (Looker / Superset)     (Redis / Feast)
```

---

# Data Layer Processing Standards

Data transformations must follow a strict, non-skippable progression:

1. **Raw Ingest**: Data lands in S3 as immutable raw logs or Parquet files. No user or pipeline may edit files in this bucket.
2. **Lakehouse Table Formats**: Apache Iceberg metadata directories index files to support dynamic transactions, schema evolution checks, and time-travel queries.
3. **dbt Transformation Layers**:
   - Staging models clean datatypes and standardize naming.
   - Intermediate models compile joins.
   - Mart tables group datasets into Fact and Dimension tables (NES-701) to support user queries.

---

# Governance & Security Integration

All elements in the Data Reference Architecture map to our governance platforms:

- **Catalog Discovery**: AWS Glue and Snowflake tables sync schema details to the DataHub metadata catalog weekly.
- **Lineage Tracing**: Airflow schedulers and dbt runs output run metadata to Marquez/OpenLineage systems.
- **Dynamic Masking**: Enforce masking policies on columns containing customer PII, protecting sensitive data.

---

# Anti-Patterns

❌ **Direct Ingestion to Marts**: Loading raw application tables directly into final Mart schemas, bypassing cleanups, validation, and staging steps.

❌ **Running Analytics on Transactional Backends**: Directly connecting Looker dashboards to production transactional databases, causing connection bottlenecks.

❌ **Ad-hoc Transformation Scripts**: Writing isolated python scripts on Cron schedules to edit database values, bypassing version-controlled dbt models.

---

# Production Checklist

- [ ] Data flow pipelines conform to the Data Reference Architecture blueprint.
- [ ] AWS Glue Data Catalog tracks all active Lakehouse schemas.
- [ ] dbt transformation models are structured in staging, intermediate, and marts layers.
- [ ] OpenLineage integration is active on Airflow schedulers.
- [ ] Row-Level Security (RLS) is active on multi-tenant marts.

---

# Success Criteria

The Data Engineering Reference Architecture is successful when:
- New pipelines integrate with data lakes, warehouses, and catalogs out-of-the-box.
- Downstream reports use verified data values compiled through dbt staging gates.
- Database query costs scale linearly and remain within monthly limits.

---

# Document Status

**Document:** NES-712 — Reference Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-800 — QA Principles**
