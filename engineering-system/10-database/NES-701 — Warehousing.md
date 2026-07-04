---
document_id: NES-701
title: Warehousing
subtitle: Enterprise Data Warehousing, Star Schema & Query Optimization Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Data Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-700 Data Platform
next_document: NES-702 ETL
---

# NES-701 — Warehousing

> **"Analytical queries require structured historical schemas. We build scaled data warehouses using dimensional modeling and optimized partition boundaries."**

---

# Executive Summary

Analytical queries (e.g. calculating yearly user retention, generating sales reports, running cohort analysis) search across millions of historical records.

Executing these queries on normalized transactional databases causes database locks and poor performance.

We mandate the execution of historical analytics inside our centralized **Data Warehouse** (powered by **Snowflake / BigQuery**).

This standard defines our dimensional modeling layouts, table partitioning strategies, and query optimization rules.

---

# Purpose

This standard defines:

- Warehouse platforms configuration (Snowflake / BigQuery)
- Dimensional Modeling (Star Schema vs. Snowflake Schema)
- Table Partitioning and Clustering keys
- Query Performance Tuning
- Compute Warehouse Auto-Scaling Rules

---

# Dimensional Modeling (Star Schema)

All warehouse datastores must be designed using **Dimensional Modeling** structures to optimize read execution speed:

- **Fact Tables**: Store quantitative measurements, events, and metrics (e.g., `fact_invoices`, `fact_student_grades`). These tables are thin, contain millions of rows, and store numeric metrics and foreign key links.
- **Dimension Tables**: Store descriptive context, attributes, and entities (e.g., `dim_students`, `dim_schools`, `dim_calendar`).

```text
       ┌──────────────────┐
       │   dim_students   │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐      ┌──────────────────┐
       │  fact_invoices   │◄─────┤   dim_calendar   │
       └────────▲─────────┘      └──────────────────┘
                │
       ┌────────┴─────────┐
       │   dim_schools    │
       └──────────────────┘
```

---

# Partitioning & Clustering

Large fact tables must be partitioned and clustered to prevent full-table scans, reducing query costs:

- **Partition Key**: Partition tables by date (e.g. `created_date`) to ensure queries that filter by time window only scan matching directories.
- **Clustering Keys**: Define clustering keys (e.g., `tenant_id`, `school_id`) for tables larger than 1TB to maintain sorted data layouts in storage blocks.

---

# Query Optimization Standards

Write warehouse queries to minimize byte processing costs:

- **No `SELECT *`**: Always select specific columns explicitly. Data warehouses use columnar storage formats; querying all columns forces the engine to read all disk blocks, driving up bills.
- **Filter Early**: Place `WHERE` clauses as early as possible in nested queries or joins.
- **Avoid Cross Joins**: Prohibit Cartesian product joins on large fact tables.

---

# Compute Autoscaling & Resource Allocation

Cloud warehouse compute resources (Snowflake virtual warehouses, BigQuery slots) must be managed dynamically:

- **Auto-Suspend**: Configure virtual warehouses to auto-suspend after **5 minutes** of inactivity to prevent idle resource billing.
- **Multi-Cluster scaling**: Enable multi-cluster scaling (e.g., min: 1, max: 5) to handle concurrent developer queries automatically during peak morning business hours.

---

# Anti-Patterns

❌ **Direct Application DB Joins**: Joining transactional tables with historical warehouse tables in the same application query context.

❌ **Sequential Table Scans**: Querying massive un-partitioned tables using loose text filters, which increases execution costs.

❌ **Mutable Dimension History loss**: Overwriting dimension table columns (like user address) without tracking historical changes. Use Slowly Changing Dimensions (SCD Type 2) with active/inactive flags.

---

# Production Checklist

- [ ] Star Schema model diagrams are verified for all major domains.
- [ ] Large tables have defined partition boundaries.
- [ ] Auto-suspend limits are set to 5 minutes or less on compute nodes.
- [ ] SCD Type 2 tracking is active on core dimension tables.
- [ ] Query performance dashboards are active in Grafana.

---

# Success Criteria

The Data Warehousing implementation is successful when:
- Complex analytical queries execute in seconds instead of minutes.
- Columnar table structures reduce monthly analytical query costs.
- Compute warehouses scale down to zero when analytical workloads are idle.

---

# Document Status

**Document:** NES-701 — Warehousing
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-702 — ETL**
