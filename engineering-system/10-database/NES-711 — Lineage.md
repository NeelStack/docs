---
document_id: NES-711
title: Lineage
subtitle: Enterprise Data Lineage, Schema Impact Analysis & OpenLineage Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Data Engineering Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-710 Data Security
next_document: NES-712 Reference Architecture
---

# NES-711 — Lineage

> **"Every data point must trace back to its origin. We document dependencies and map data flow lineage dynamically using OpenLineage."**

---

# Executive Summary

In a complex data platform with hundreds of transactional tables, ingestion routes, transformations, and BI dashboards, tracking dependencies is critical.

If a developer alters a database column name in a backend database without knowing which downstream dbt models, ML features, or Looker dashboards rely on that field, analytical reports will break.

We mandate the tracking of **Data Lineage** across all systems.

This standard establishes our tracking protocols (**OpenLineage**), metadata catalog linkages, and downstream impact analysis rules.

---

# Purpose

This standard defines:

- Data Lineage Core Principles
- OpenLineage Integration Standards
- Column-Level Lineage Mapping
- Downstream Impact Analysis for Schema Changes
- Versioning and Lineage Documentation

---

# Lineage Core Principles

Every data asset in our ecosystem must support three lineage capabilities:

1. **Source Traceability**: Every value in a fact table or dashboard must be traceable back to its origin database table, ingestion script, and server node.
2. **Transformation Visibility**: Every SQL conversion, mapping, or calculation applied to a dataset must be recorded in the lineage history.
3. **Downstream Dependency Mapping**: System maps must show all dependencies (dbt models, BI reports, ML models) that rely on a target database table.

---

# OpenLineage Integration Standards

We standardize on **OpenLineage** as our event protocol for collecting lineage metadata at runtime.

- **Orchestrator Integration**: Enable the OpenLineage listener inside Apache Airflow. Schedulers must submit lineage metadata automatically on every task execution.
- **dbt Integration**: Extract lineage structures from dbt manifest files (`manifest.json`) during compilation to map parent-child connections.

```yaml
# Airflow configuration for OpenLineage
lineage:
  backend: openlineage.lineage.backend.OpenLineageBackend
  openlineage_url: http://marquez.data-platform.local:8080
```

---

# Column-Level Lineage Mapping

Tracing at the table level is insufficient. Lineage must drill down to the individual column level:

- **Column Maps**: System maps must track when columns are renamed, combined (e.g. joining `first_name` and `last_name` to `full_name`), or cast to alternative datatypes.
- **Benefits**: Column maps allow developers to identify if modifying a specific column type affects downstream reporting parameters.

---

# Schema Change Impact Analysis

Before deploying schema migrations (e.g., dropping columns, changing datatypes, renaming tables):

- **Lineage Check Step**: Developers must query the DataHub Lineage Graph for the target table to locate all downstream dependencies.
- **Notification SLA**: If a planned database change affects a downstream report or ML feature owned by another team, developers must notify the affected owners at least **7 days** prior to merging the change.

---

# Anti-Patterns

❌ **Blind Schema Migrations**: Dropping columns in transactional databases without verifying if they are queried by historical analytics systems.

❌ **Manual Lineage Documentation**: Relying on manual drawings or Excel sheets to map database dependencies, which become out-of-date immediately.

❌ **Exposing Raw Production Server Paths**: Printing internal database names, connection ports, or storage bucket paths in public lineage reports.

---

# Production Checklist

- [ ] OpenLineage integration is active in Apache Airflow.
- [ ] dbt compiler exports manifest data to the lineage collector.
- [ ] Schema impact analysis checks are integrated with developer review workflows.
- [ ] Table dependencies are searchable in DataHub.
- [ ] Access controls restrict administrative updates to lineage graphs.

---

# Success Criteria

The Data Lineage program is successful when:
- 100% of data transformations and data pipelines submit lineage events automatically.
- Developers can trace the impact path of column modifications prior to writing migration code.
- Outages or invalid data runs can be isolated to the source system in under 2 minutes.

---

# Document Status

**Document:** NES-711 — Lineage
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-712 — Data Engineering Reference Architecture**
