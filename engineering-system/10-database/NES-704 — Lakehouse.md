---
document_id: NES-704
title: Lakehouse
subtitle: Enterprise Lakehouse, Apache Iceberg & Metadata Catalog Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Data Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-703 ELT
next_document: NES-705 Analytics
---

# NES-704 — Lakehouse

> **"Data lakes store cost-effectively, data warehouses structure efficiently. We merge both into a single Data Lakehouse using open table formats."**

---

# Executive Summary

Storing raw multi-terabyte datasets in traditional cloud databases or proprietary data warehouses leads to high storage costs.

Conversely, unstructured raw data lakes (files in S3 folders) lack transaction boundaries, schema safety, metadata indexes, and update capabilities.

We mandate the adoption of a **Data Lakehouse** architecture.

This standard defines our open table formats (**Apache Iceberg**), metadata catalog configurations, query engines (**Trino / AWS Athena**), and file optimization rules.

---

# Purpose

This standard defines:

- Lakehouse Architecture and Principles
- Open Table Formats Selection (Apache Iceberg)
- Metadata Catalog Configurations (AWS Glue)
- Query Engine Standards (AWS Athena / Trino)
- Compaction and Storage Optimizations

---

# Lakehouse Architecture

The Data Lakehouse merges the storage economics of a Data Lake (S3 storage) with the ACID transactional benefits of a Data Warehouse.

```text
 ┌──────────────────────────────────────────────┐
 │    Query Layer (AWS Athena / Trino / Spark)  │
 ├──────────────────────────────────────────────┤
 │      Catalog Layer (AWS Glue Metadata)       │
 ├──────────────────────────────────────────────┤
 │  Table Format Layer (Apache Iceberg Metadata)│
 ├──────────────────────────────────────────────┤
 │       Storage Layer (Amazon S3 Parquet)      │
 └──────────────────────────────────────────────┘
```

---

# Table Format Standard (Apache Iceberg)

All tables inside the analytical Data Lake must be formatted using the **Apache Iceberg** specification.

- **ACID Transactions**: Enables safe concurrent read/write transactions, rollback updates, and dynamic inserts inside S3.
- **Schema Evolution**: Supports renaming or adding columns without breaking historical queries or requiring full table rewrites.
- **Partition Evolution**: Automatically updates partition layouts as queries change over time without requiring rebuilding tables.

---

# Metadata Catalog Configuration

We use **AWS Glue Data Catalog** as the centralized directory for all lakehouse table schemas.

- **Sync Policy**: Ingestion pipelines must sync table schema alterations to the Glue Catalog automatically.
- **Single Source**: Schedulers, Spark jobs, and Athena query nodes must pull metadata descriptions from the centralized Glue Catalog to ensure schema alignment.

---

# Query Engine Standards (AWS Athena)

We use **Amazon Athena** (serverless Presto/Trino) for executing ad-hoc sql queries against the Lakehouse.

- **Athena Configuration**: Configure query result locations to automatically expire after 7 days in S3 bucket settings.
- **Cost Allocation**: Group queries into distinct Athena Workgroups (e.g. `engineering-queries`, `reporting-queries`) to trace monthly costs and enforce billing limits per team.

---

# File Compaction & Storage Optimization

Streaming pipelines create thousands of small files in S3 directories, which slows down query engines due to directory seek overhead.

- **Daily Compaction**: SRE schedule daily Spark compaction tasks to combine small parquet files into optimized larger blocks (typically **128MB – 512MB**).
- **Parquet Compression**: Compress all parquet data files using **Snappy** or **ZSTD** compression engines.

---

# Anti-Patterns

❌ **Direct CSV Querying**: Querying raw CSV files directly via Athena. CSV files are uncompressed and lack column indexing, which increases query costs. Always convert raw inputs to Parquet formats.

❌ **Excluding Table Catalogs**: Querying S3 paths directly without registering them in the metadata catalog, creating untracked files.

❌ **Hardcoded Schema Definitions**: Creating Athena tables manually without schema validation, leading to query failures when upstream databases alter columns.

---

# Production Checklist

- [ ] All data lake tables utilize the Apache Iceberg format.
- [ ] AWS Glue Data Catalog stores all active table metadata schemas.
- [ ] Compression (ZSTD/Snappy) is configured for Parquet generation pipelines.
- [ ] Compaction schedulers are active for high-throughput tables.
- [ ] Query workgroups have defined monthly billing thresholds.

---

# Success Criteria

The Lakehouse implementation is successful when:
- Queries execute across multi-terabyte datasets without requiring database imports.
- Storage costs are maintained at object storage levels rather than warehouse database pricing limits.
- Upstream schema alterations propagate automatically across query engines.

---

# Document Status

**Document:** NES-704 — Lakehouse
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-705 — Analytics**
