---
document_id: NES-708
title: Feature Store
subtitle: Enterprise Feature Store, Feast & Online/Offline Sync Standard
version: 1.0.0
status: Draft
classification: Internal
owner: AI & Data Science Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-707 ML Pipelines
next_document: NES-709 Data Governance
---

# NES-708 — Feature Store

> **"Consistent features produce consistent predictions. We centralize, register, and synchronize ML features using Feast and unified online/offline stores."**

---

# Executive Summary

Machine Learning (ML) models require structured data parameters ("features") to generate predictions.

If data scientists write custom SQL queries to extract features for training while application developers write separate SQL queries to extract features for live production APIs, feature mismatch occurs, leading to prediction errors.

We mandate the centralization of all machine learning features inside a **Feature Store** (powered by **Feast / Hopsworks**).

This standard defines feature registrations, low-latency online stores (**Redis**), and offline historical stores (**S3/Snowflake**).

---

# Purpose

This standard defines:

- Feature Store Architecture (Feast)
- Feature Definition and Registration
- Online Low-Latency Store Configuration (Redis)
- Offline Historical Store Configuration (S3/Snowflake)
- Feature Synchronization (Materialization)

---

# Feature Store Architecture

The Feature Store decouples feature calculation from models, serving consistent features across training and inference.

```text
 ┌──────────────────────┐      ┌──────────────────────┐
 │   Batch Ingestion    │      │  Real-Time Ingestion │
 └──────────┬───────────┘      └──────────┬───────────┘
            ▼                             ▼
 ┌──────────────────────┐      ┌──────────────────────┐
 │    Offline Store     │      │     Online Store     │
 │ (S3 / Snowflake)     │      │       (Redis)        │
 │  - Best for Training │      │  - Best for APIs     │
 └──────────────────────┘      └──────────────────────┘
```

---

# Feature Definition & Registration

All features must be declared as code inside the feature repository.

- **Declarative Code**: Define features using Python configurations and check them into the Git repository.
- **Entity Association**: Every feature must link to an entity primary key (e.g. `student_id`, `school_id`, `tenant_id`).
- **Unified Types**: Specify strict datatypes (e.g. Float, Int64, String) to prevent data corruption between online and offline stores.

---

# Offline Store (For Model Training)

The offline store manages historical feature tables:

- **Storage**: Maps to our Parquet Data Lake or Snowflake analytical warehouse.
- **Point-in-Time Joins**: When building training datasets, query the offline store using point-in-time joins ("time-travel") to prevent data leakage (using future data to predict historical events).

---

# Online Store (For Live API Predictions)

The online store serves features at high speed to active APIs:

- **Storage**: Powered by **Amazon ElastiCache (Redis)**.
- **Latency Target**: Serving time must remain under **10ms**.
- **Materialization Schedulers**: Configure Airflow schedulers to execute materialization tasks (e.g. `feast materialize`) hourly, reading recent calculations from the offline store and writing them to the online Redis store.

```bash
# Command to materialize features to Redis
feast materialize 2026-01-01T00:00:00 2026-07-04T00:00:00
```

---

# Anti-Patterns

❌ **Ad-hoc Feature SQL in APIs**: Writing duplicate database joins inside backend APIs to query features, bypassing the online Redis store.

❌ **Future Data Leakage**: Querying dimensions without filtering by the exact historical timestamp of the training event, introducing future parameters into model training runs.

❌ **Excluding Schema Verification**: Registering features without schema declarations, causing prediction failures when data columns mutate.

---

# Production Checklist

- [ ] Feature store registry (Feast) is versioned in Git.
- [ ] Online store runs on Amazon ElastiCache (Redis).
- [ ] Offline store is linked to Snowflake/S3 tables.
- [ ] Materialization schedules are configured.
- [ ] Feature serving latencies are monitored in Grafana.

---

# Success Criteria

The Feature Store implementation is successful when:
- Training and live APIs retrieve identical feature metrics for shared entities.
- Feature query latencies for live API endpoints remain under 10ms.
- Point-in-time data checks confirm zero future data leakage in training datasets.

---

# Document Status

**Document:** NES-708 — Feature Store
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-709 — Data Governance**
