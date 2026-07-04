---
document_id: NES-700
title: Data Platform
subtitle: Enterprise Data Platform Architecture, Storage Tiering & Pipeline Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Data Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-616 Security Reference Architecture
next_document: NES-701 Warehousing
---

# NES-700 — Data Platform

> **"Data is the foundation of platform intelligence. We build a unified, tier-structured data platform that serves analytics, reporting, and AI models securely."**

---

# Executive Summary

As the NeelStack ecosystem scales across education, healthcare, and SaaS products, the volume of transactional records, audit trails, unstructured documents, and analytical events grows exponentially.

If every product implements its own isolated databases and analytics queues, data silos will emerge, causing duplicate pipelines, high infrastructure bills, and sync conflicts.

We mandate the adoption of a unified **NeelStack Data Platform** architecture.

This standard outlines the storage tiering guidelines, pipeline architectures, data access limits, and platform integrations.

---

# Purpose

This standard defines:

- Data Platform Core Layers
- Storage Tiering Strategy (Hot, Warm, Cold)
- Data Ingestion Pipelines
- Data Access Security boundaries
- Platform Integration APIs

---

# Data Platform Core Layers

The Data Platform is divided into four distinct compute and storage layers:

```text
  ┌─────────────────────────────────────────────────────────┐
  │  Ingestion Layer (Kafka Events, Debezium CDC, API logs) │
  ├─────────────────────────────────────────────────────────┤
  │  Storage Layer (RDS Postgres, S3 Data Lake, OpenSearch) │
  ├─────────────────────────────────────────────────────────┤
  │  Processing Layer (Airflow, Spark, dbt transformations) │
  ├─────────────────────────────────────────────────────────┤
  │  Serving Layer (BI Dashboards, API endpoints, AI models)│
  └─────────────────────────────────────────────────────────┘
```

---

# Storage Tiering Strategy

We optimize storage costs and performance by tiering data based on access frequency and age:

### 1. Hot Storage (Real-time Transactional)
- **Technology**: PostgreSQL (Amazon RDS), Redis.
- **Latency Target**: Sub-second (e.g. 10ms - 50ms).
- **Data Scope**: Active user profiles, session states, recent documents, pending invoices.

### 2. Warm Storage (Operational Analytics)
- **Technology**: OpenSearch / Elasticsearch, S3 Parquet tables.
- **Latency Target**: Seconds (e.g. 1s - 5s).
- **Data Scope**: Historical logs, audit trails (past 30 days), full-text search indexes.

### 3. Cold Storage (Analytical Data Lake)
- **Technology**: Snowflake, Amazon S3 (Apache Iceberg format), Glacier.
- **Latency Target**: Minutes to Hours.
- **Data Scope**: Multi-year transaction histories, raw analytical events, backup archives.

---

# Ingestion Pipeline Architecture

Data enters the platform via two ingestion models:

- **Streaming Ingestion**: Real-time event streams (like user clicks or API telemetry) write to **Apache Kafka (NES-211)** topics. Downstream consumers digest and write payloads to OpenSearch or S3.
- **Change Data Capture (CDC)**: Transactional updates inside primary PostgreSQL databases are streamed in real-time to the data lake using **Debezium**, bypassing origin application CPUs.

---

# Data Access Security

Protect raw database schemas from unauthorized queries:

- **No Direct Prod DB Queries**: Business intelligence (BI) systems, analytics scripts, and reporting tools must *never* query production transactional databases directly.
- **Serving Layer isolation**: Analytics tools must query warm or cold datastores (OpenSearch or Snowflake warehouses) configured with read-only credentials, protecting production transactions from resource locks.

---

# Anti-Patterns

❌ **Storing Raw Logs in Transactional DBs**: Saving high-volume log strings or audit tables inside primary PostgreSQL tables, causing database size bloat and sluggish backups.

❌ **Omitting Data Lifecycle Policies**: Leaving historical analytics logs inside hot databases indefinitely, driving up cloud storage costs.

❌ **Ad-hoc File Ingestion**: Copying CSV dumps manually into S3 without registering them in the metadata catalog, creating "data swamps."

---

# Production Checklist

- [ ] Storage tiering structures are configured and active.
- [ ] Debezium CDC configuration is operational on production databases.
- [ ] Analytics queries are routed to read-only replica databases or warehouses.
- [ ] KMS encryption is active on all data stores.
- [ ] Ingestion pipelines monitor and alert on data drop anomalies.

---

# Success Criteria

The Data Platform implementation is successful when:
- High-volume analytical queries execute successfully without affecting transactional database performance.
- Egress storage costs are minimized using automatic S3 lifecycle transitions.
- Data pipelines maintain complete ingestion traceability from producer to data lake.

---

# Document Status

**Document:** NES-700 — Data Platform
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-701 — Warehousing**
